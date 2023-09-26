package main

import (
    "html/template"
    "net/http"
)

func homePage(w http.ResponseWriter, r *http.Request) {
    tmpl, err := template.ParseFiles("index.html")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    tmpl.Execute(w, nil)
}

func search(w http.ResponseWriter, r *http.Request) {
    // Retrieve the search query entered by the user
    query := r.URL.Query().Get("query")

    // Process the query and fetch results (you'll need to fill in this part according to your own search logic)

    // Display the results using the results.html template
    tmpl, err := template.ParseFiles("results.html")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    // Send the results in a data structure
    data := struct {
        Results []struct {
            Link  string
            Title string
        }
    }{
        // Populate the results here
        // For example: {Link: "http://example.com", Title: "Example Page"}
    }
    tmpl.Execute(w, data)
}

func main() {
    http.HandleFunc("/", homePage)
    http.HandleFunc("/search", search)

    http.ListenAndServe(":8080", nil)
}
