(defproject convert-climate-data "1.0"
  :description "convert climate data from one grid per day and climate element format to one csv file with all climate data per pixel"
  :url ""
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [clj-time "0.6.0"]
                 [clojure-csv "2.0.1"]
                 [netcdf-clj "0.0.11"]]
  :main ^:skip-aot convert.ascii-grids
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})






