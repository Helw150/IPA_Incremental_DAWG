package main


import (
	"metalang.io/dawg"
	"os"
	"os/exec"
	"encoding/json"
	"io/ioutil"
	"fmt"
)

type QueryList struct{
	File_ids interface{}
	Queries map[string][]string
}

func stringInSlice(str string, list []string) bool {
 	for _, v := range list {
 		if v == str {
 			return true
 		}
 	}
 	return false
}
func main() {
	var PrecisionSum float32
	var RecallSum float32
	PrecisionSum = 0.0
	RecallSum = 0.0
	SearchTermFile := os.Args[1]
	IndexFile := os.Args[2]
	raw, _ := ioutil.ReadFile(SearchTermFile)
	var f QueryList
	json.Unmarshal(raw, &f)
	fmt.Println(len(f.Queries))
	for k := range f.Queries {
		var matches []string
		var err error
		var Precision float32
		Precision = 1.0
		TruePositive := 0
		FalsePositive := 0
		fmt.Println(k)
		cmd := exec.Command("python", "search/SearchTermCreation.py", k)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		NoFile := cmd.Run()
		if NoFile == nil {
			matches, err = dawg.SearchFile(IndexFile, k)
		}
		if err != nil {
			PrecisionSum += 1.0
			continue
		}
		fmt.Println("Keyword = ", k)
		RealMatches := len(f.Queries[k])
		fmt.Println("RealMatches = ", RealMatches)
		for _, match := range matches{
			if stringInSlice(match, f.Queries[k]){
				TruePositive++
				fmt.Println("TruePositive = ", TruePositive)
			} else {
				FalsePositive++
			}
		}
		if TruePositive + FalsePositive != 0 {
			Precision = float32(TruePositive) / float32(TruePositive + FalsePositive)
		}
		Recall := float32(TruePositive) / float32(RealMatches)
		PrecisionSum += Precision
		RecallSum += Recall
		fmt.Println("Precision = ", Precision)
		fmt.Println("Recall = ", Recall)
	}
	TotalPrecision := PrecisionSum / float32(len(f.Queries))
	TotalRecall := RecallSum / float32(len(f.Queries))
	fmt.Println("TotalPrecision = ", TotalPrecision)
	fmt.Println("TotalRecall = ", TotalRecall)
}
