(ns convert.ascii-grids
  (:gen-class)
  (:require [clojure.edn :as edn]
            [clojure.java.io :as io]
            [clojure.string :as cs]
            [clj-time.core :as ctc]
            [clojure-csv.core :as csv]
            [clj-time.coerce :as ctcoe]
            [clj-time.format :as ctf]))

(defn write-files-test
  [{:keys [data-dir rows cols append? content newline?]}]
  (let [data-dir (or data-dir #_(edn/read-string data-dir) "data")
        append? (or (edn/read-string append?) false)
        nl? (edn/read-string newline?)
        newline? (if (nil? nl?) true nl?)
        content (str (or content "x") (when newline? \newline))]
    (doseq [r (range (edn/read-string rows)) c (range (edn/read-string cols))
            :let [path-to-file (str data-dir "/row-" r "/col-" c ".txt")]]
      (do
        (when-not append? (io/make-parents path-to-file))
        (spit path-to-file content :append append?)))))

(defn read-files-test
  [{:keys [data-dir rows cols]}]
  (let [data-dir (or data-dir #_(edn/read-string data-dir) "data")]
    (doseq [r (range (edn/read-string rows)) c (range (edn/read-string cols))
            :let [path-to-file (str data-dir "/row-" r "/col-" c ".txt")]]
      (slurp path-to-file))))


(defn make-file-name [path sym d m y]
  (str path y (when (< m 10) 0) m (when (< d 10) 0) d "_" (name sym) "_sa.asc"))

(def opened-files (atom {}))
(def line-seqs (atom {}))

(defn open-files [path folder-suffix from-year to-year from-diy to-diy]
  (doseq [sym [:gs :ws :t2m_hk :tmin :tmax :p :rh]
          year (range from-year (inc to-year))
          :let [leap-year? (.. (ctc/date-time year) year isLeap)
                days-in-year (if leap-year? 366 365) #_(.. (ctc/date-time year) year toInterval toDuration getStandardDays)]
          diy (range (max 1 from-diy) (inc (min to-diy days-in-year)))
          :let [date (ctc/plus (ctc/date-time year 1 1) (ctc/days (dec diy)))
                date* (ctcoe/to-long date)
                [day month] ((juxt ctc/day ctc/month) date)
                rdr (clojure.java.io/reader (make-file-name (str path "/" (name sym) folder-suffix "/") sym day month year))]]
    (swap! opened-files assoc-in [sym date*] rdr)
    (swap! line-seqs assoc-in [sym date*] (line-seq rdr)))
  (println "opened all fiwles from year " from-year " to year " to-year " and from diy " from-diy " to " to-diy))


(defn close-files []
  (doseq [[sym rdrs] @opened-files
          [_ rdr] rdrs]
    (.close rdr)))

(defn create-row-strs [{:keys [tmin t2m_hk tmax p rh ws gs] :as row}]
  (map (fn [[date* tmin] [_ tavg] [_ tmax] [_ p] [_ gs] [_ rh] [_ ws]]
         (let [date (ctcoe/from-long date*)
               date-str (ctf/unparse (ctf/formatter "dd.MM.yyyy") date)]
           (map str [(ctc/day date) (ctc/month date) (ctc/year date) date-str tmin tavg tmax p gs rh ws])))
       tmin t2m_hk tmax p gs rh ws))

(defn drop-rows
  "drops a the given amount of rows and the 6 initial header rows"
  [rows-to-drop]
  (doseq [[sym lseqs] @line-seqs
          [date* lseq] lseqs]
    (swap! line-seqs update-in [sym date*]
           #(do
             (println "droping from file sym/date " sym "/"
                      (ctf/unparse (ctf/formatter "dd.MM.yyyy") (ctcoe/from-long date*)))
             (drop (+ 6 rows-to-drop) %))))
  (println "droped " (+ 6 rows-to-drop)))

(def fmap
  (fn [f m]
    (into (sorted-map)
          (map (fn [[k v]]
                 [k (f v)])
               m))))

(def csv-header
  ["day" "month" "year" "date" "tmin" "tavg" "tmax" "precip" "globrad" "relhumid" "windspeed"])

(defn write-climate-files* [path start-at-row write-max-rows skip-header?]
  (loop [row-count start-at-row] ;loop over rows in all files
    (if (or (= (- row-count start-at-row) write-max-rows)
            (-> @line-seqs :gs first second nil?))
      :ready
      (let [;create a functional map with seqs for the columns of a row
            #__ #_(doseq [[s m] @line-seqs]
                    (println "sym: " s)
                    (doseq [[d v] m]
                      (print d " ")
                      (-> v first (cs/split,,, #"\s+"))))
            row (fmap #(fmap (fn [v] (-> v first (cs/split ,,, #"\s+"))) %) @line-seqs)]
        ;loop recursivly through all cols
        (loop [cols row
               col-count 0] ;loop over the cols in all files
          (if (-> cols :gs first second nil?)
            :ready
            (let [row-strs (create-row-strs (fmap #(fmap first %) cols))
                  path-to-file (str path "/row-" row-count "/col-" col-count ".txt")
                  _ (io/make-parents path-to-file)]
              (with-open [w (clojure.java.io/writer path-to-file :append true)]
                (when-not skip-header? (.write w (csv/write-csv [csv-header])))
                (doseq [row-str row-strs]
                  (.write w (csv/write-csv [row-str]))))
              (recur (fmap #(fmap next %) cols) (inc col-count)))))
        ;update the row pointer imperatively to point to the next row
        (doseq [[sym lseqs] @line-seqs
                [date* lseq] lseqs]
          (swap! line-seqs update-in [sym date*] next))
        ;and recur
        (println "wrote/updated row " row-count)
        (recur (inc row-count))))))


(defn run-climate-file-conversion [{:keys [read-path read-folder-suffix write-path from-year to-year from-diy to-diy from-row to-row skip-header?]}]
  (let [read-path (or read-path "in-data")
        read-folder-suffix (or read-folder-suffix "_2001-2040")
        write-path (or write-path "out-data")
        from-year (or (edn/read-string from-year) 2013)
        to-year (or (edn/read-string to-year) 2040)
        from-diy (or (edn/read-string from-diy) 1)
        to-diy (or (edn/read-string to-diy) 366) ;the correct number of days in year is calculated and overwrites 366 if necessary
        from-row (or (edn/read-string from-row) 0)
        to-row (or (edn/read-string to-row) (dec 2545))
        skip-header? (or (edn/read-string skip-header?) false)]
    (open-files read-path read-folder-suffix from-year to-year from-diy to-diy)
    (drop-rows from-row)
    (write-climate-files* write-path from-row (max 0 (- (inc to-row) from-row)) skip-header?)
    (close-files)))

(defn -main2
  [& kvs]
  (let [options (reduce (fn [m [k v]]
                          (assoc m (keyword k) v))
                        {} (partition 2 kvs))]
    (case (:test options)
      "read" (doseq [t (range 1 (edn/read-string (or (:count options) "4")))]
               (.start (Thread. (partial read-files-test options #_(assoc options :data-dir (str "data-" t))))))
      "write" (write-files-test options)
      "conversion" (run-climate-file-conversion options)
      nil (write-files-test options))))

(defn -main
  [& kvs]
  (let [options (reduce (fn [m [k v]]
                          (assoc m (keyword k) v))
                        {} (partition 2 kvs))]
    (case (:test options)
      "read" (doseq [t (range 1 (edn/read-string (or (:count options) "4")))]
               (.start (Thread. (partial read-files-test options #_(assoc options :data-dir (str "data-" t))))))
      "write" (write-files-test options)
      "conversion" (run-climate-file-conversion options)
      nil (write-files-test options))))


#_(-main "test" "conversion" "read-path" "f:/" "read-folder-suffix" "_2001-2040"
         "write-path" "f:/climate-data-years-2001-2040-rows-0-499"
         "from-year" "2001" "to-year" "2003"
         "from-row" "0" "to-row" "499"
         "skip-header?" "false")

#_(-main :rows "10" :cols "10" :append? "true" :content "a")












