(ns convert.netcdf
  (:gen-class)
  (:require [clojure.edn :as edn]
            [clojure.java.io :as io]
            [clojure.string :as cs]
            [clj-time.core :as ctc]
            [clojure-csv.core :as csv]
            [clj-time.coerce :as ctcoe]
            [clj-time.format :as ctf]
            [netcdf.dataset :as nd]))

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

(def opened-datasets (atom {}))
(def variables (atom {}))

(defn open-files [path from-year to-year]
  (doseq [[filename-start sym var-name unit]
          [["ASWDIFD_S_ts_" :aswdifd_s "ASWDIFD_S" :W_m-2]
           ["ASWDIR_S_ts_" :aswdir_s "ASWDIR_S" :W_m-2]
           ["DURSUN_ts_" :dursun "DURSUN" :s]
           ["RELHUM_2M_ts_" "RELHUM_2M" :relhum_2m :%]
           ["T_2M_ts_" "T_2M" :t_2m :K]
           ["TD_2M_ts_" "TD_2M" :td_2m :K]                      ; dew point temp = Taupunkt
           ["TOT_PREC_ts_" "TOT_PREC" :tot_prec :kg_m-2]           ; total precipition
           ["U_10M_ts_" "U_10M" :u_10m :m_s-1]                  ; wind u component 10m
           ["V_10M_ts_" "V_10M" :v_10m :m_s-1]                  ; wind v component 10m
           ]
          year (range from-year (inc to-year))
          :let [dataset (nd/open-dataset (str path "/" filename-start year))]]
    (swap! opened-datasets assoc-in [year sym] dataset)
    (swap! variables assoc-in [sym year] (.findVariable dataset var-name)))
  (println "opened all datasets from year " from-year " to year " to-year))


(defn close-files []
  (doseq [[year syms] @opened-datasets
          [_ dataset] syms]
    (.close dataset)))

(defn create-row-strs [{:keys [tmin t2m_hk tmax p rh ws gs] :as row}]
  (map (fn [[date* tmin] [_ tavg] [_ tmax] [_ p] [_ gs] [_ rh] [_ ws]]
         (let [date (ctcoe/from-long date*)
               date-str (ctf/unparse (ctf/formatter "dd.MM.yyyy") date)]
           (map str [(ctc/day date) (ctc/month date) (ctc/year date) date-str tmin tavg tmax p gs rh ws])))
       tmin t2m_hk tmax p gs rh ws))

(def fmap
  (fn [f m]
    (into (sorted-map)
          (map (fn [[k v]]
                 [k (f v)])
               m))))

(def csv-header
  ["day" "month" "year" "date" "tmin" "tavg" "tmax" "precip" "globrad" "relhumid" "windspeed"])

(defn write-climate-files* [path from-year to-year start-at-row write-max-rows skip-header?]
  (doseq [lat (range 0 441)
          lon (range 0 400)]

    (doseq [year (range from-year (inc to-year))]
    (let [leap-year? (.. (ctc/date-time year) year isLeap)
          days-in-year (if leap-year? 366 365)
          sym-to-var (variables year)

          to-seq-3 (fn [arr]
                   (for [i (range 0 (.getSize arr))]
                     (.get arr i lat lon)))

          to-seq-4 (fn [arr]
                     (for [i (range 0 (.getSize arr))]
                       (.get arr i 0 lat lon)))




          sum (fn [arr rank]
                (case rank
                  3 (reduce (fn [[vs acc] i]
                              (let [mod-i (mod (inc i) 24)
                                    hour (if (= mod-i 0) 23 (dec i))
                                    s (+ acc (.get arr hour lat lon))]
                                (if (= mod-i 0)
                                  [(conj vs s) 0]
                                  [vs s])))
                            [[] 0] (range 0 (.getSize arr)))
                  4 (reduce (fn [[vs acc] i]
                              (let [mod-i (mod (inc i) 24)
                                    hour (if (= mod-i 0) 23 (dec i))
                                    s (+ acc (.get arr hour 0 lat lon))]
                                (if (= mod-i 0)
                                  [(conj vs s) 0]
                                  [vs s])))
                            [[] 0] (range 0 (.getSize arr)))))

          avg (fn [var rank]
                (case rank
                  3 (/ (reduce (fn [acc hour] (+ acc (.get var hour lat lon))) 0 (range 0 24)) 24)
                  4 (/ (reduce (fn [acc hour] (+ acc (.get var (dec hour) 0 lat lon))) 0 (range 1 (inc 24))) 24)))

          mma-t (fn [t2m]
                  (reduce (fn [[mins maxs avgs vs] i]
                            (let [mod-i (mod (inc i) 24)
                                  hour (if (= mod-i 0) 23 (dec i))
                                  v (+ acc (.get t2m hour lat lon))]
                              (if (= mod-i 0)
                                (let [vs* (conj vs v)]
                                  [(conj mins (min vs*))
                                   (conj maxs (max vs*))
                                   (conj avgs (/ (reduce + 0 vs*) 24))
                                   []])
                                [mins maxs avgs (conj vs v)])))
                          [[] [] [] []] (range 0 (.getSize arr))))

          rad (fn [dir dif lat lon]
                (reduce (fn [acc hour] (+ acc
                                          (.get dir hour lat lon)
                                          (.get dif hour lat lon)))
                        0 (range 0 24)))

          ;get all data for a single year (hourly values)
          t2m (-> sym-to-var :t_2m (.read ,,, (str ":,0," lat "," lon) to-seq-4 (#(partition 24 %))))
          dir-rad (-> sym-to-var :aswdir_s (.read ,,, (str ":," lat "," lon)))
          dif-rad (-> sym-to-var :aswdifd_s (.read ,,, (str ":," lat "," lon)))
          dursun (-> sym-to-var :dursun (.read ,,, (str ":," lat "," lon)))
          relhum (-> sym-to-var :relhum (.read ,,, (str ":,0," lat "," lon)))
          tot-prec (-> sym-to-var :tot_prec (.read ,,, (str ":," lat "," lon)))
          u-wind (-> sym-to-var :tot_prec (.read ,,, (str ":,0," lat "," lon)))
          v-wind (-> sym-to-var :tot_prec (.read ,,, (str ":,0," lat "," lon)))



          ]
      (doseq [diy (range 1 (inc days-in-year))]
        (let [date (ctc/plus (ctc/date-time year) (ctc/days (dec diy)))
              day (ctc/day date)
              month (ctc/month date)
              iso-date-str (ctf/unparse (ctf/formatter "yyyy-MM-dd") date)
              ; get for the current day in the year all lat/long values (hourly values, which have to be aggregated)
              t2m (-> sym-to-var :t_2m (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) ",0," lat "," lon)))

              dir-rad (-> sym-to-var :aswdir_s (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) "," lat "," lon)))
              dif-rad (-> sym-to-var :aswdifd_s (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) "," lat "," lon)))
              dursun (-> sym-to-var :dursun (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) "," lat "," lon)))
              relhum (-> sym-to-var :relhum (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) ",0," lat "," lon)))
              tot-prec (-> sym-to-var :tot_prec (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) "," lat "," lon)))
              u-wind (-> sym-to-var :tot_prec (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) ",0," lat "," lon)))
              v-wind (-> sym-to-var :tot_prec (.read ,,, (str (* (dec diy) 24) ":" (dec (* diy 24)) ",0," lat "," lon)))
              ]



          )

        )




      )))


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
    ;(drop-rows from-row)
    (write-climate-files* write-path from-row (max 0 (- (inc to-row) from-row)) skip-header?)
    (close-files)))

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












