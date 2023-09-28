package main

import (
	"bufio"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type Result struct {
	Link  string
	Title string
}

type ResultData struct {
	Results []Result
}

func homePage(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("index.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}

func listFilesInDirectory(directoryPath string, searchString string) ([]Result, error) {
	var result_list []Result

	// Dizindeki dosyaları okuyoruz
	files, err := ioutil.ReadDir(directoryPath)
	if err != nil {
		log.Fatal(err)
	}

	// Dosyaları tek tek okuyup searchString ifadesini içeriyorlar mı kontrol et
	for _, file := range files {
		just_filename := file.Name()

		file_path, err := filepath.Abs(directoryPath + "/" + file.Name())
		if err != nil {
			panic(err)
		}

		file, err := os.Open(file_path)
		if err != nil {
			log.Printf("Dosya açma hatası: %v", err)
			break
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		// Satır satır aradığımız ifadeyi araştıralım
		for scanner.Scan() {
			query_string := string(searchString)
			line := scanner.Text()

			line = strings.ToLower(line)
			query_string = strings.ToLower(query_string)

			if strings.Contains(line, query_string) {
				title := query_string + " - " + just_filename
				link := "/index-db/" + just_filename
				result_list = append(result_list, Result{Title: title, Link: link})
				break
			}
		}
		if err := scanner.Err(); err != nil {
			log.Printf("Dosya okuma hatası: %v", err)
		}
	}
	return result_list, nil
}

func search(w http.ResponseWriter, r *http.Request) {
	// Aradığımız şey
	searchString := r.URL.Query().Get("query")

	// Arama algoritması - Sonuçları index db'den çekiyoruz
	directoryPath := "./index-db"

	result_list, err := listFilesInDirectory(directoryPath, searchString)
	if err != nil {
		log.Fatalf("Dizin listeleme hatası: %v", err)
	}

	// Sonuçları Başlık & Link olarak listeliyoruz.
	tmpl, err := template.ParseFiles("results.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Sonucları göster
	data := ResultData{
		Results: result_list,
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func main() {
	http.HandleFunc("/", homePage)
	http.HandleFunc("/search", search)

	// index-db içindeki dosyaları serve et:
	fs := http.FileServer(http.Dir("index-db"))
	http.Handle("/index-db/", http.StripPrefix("/index-db/", fs))

	http.ListenAndServe(":8080", nil)
}
