package dawg

import "testing"
import "metalang.io/levenshtein"

func TestCreateDAWG(t *testing.T) {
	dawg := CreateDAWG([]string{"test", "rest", "nest", "note"})
	if dawg.nodesCount != 8 {
		t.Error("Creation failed")
	}
}

func TestSearch(t *testing.T) {
	dawg := CreateDAWG([]string{"test", "tese", "nest", "test2", "tes", "note"})

	test, err := dawg.Search("test", 0, 1, false, false)
	if err != nil || len(test) != 1 || test[0] != "test" {
		t.Error("Search failed")
	}
}

func TestIncrementalSearch(t *testing.T) {
	dawg := CreateDAWG([]string{"test", "tese", "nest", "test2", "tes", "note"})
	test, err := dawg.IncrementalSearch(dawg.initialState, 't')
	test, err = dawg.IncrementalSearch(test, 'e')
	test, err = dawg.IncrementalSearch(test, 's')
	test, err = dawg.IncrementalSearch(test, 't')
	if err != nil || !(test.final) {
		t.Error("Incremental Search failed")
	}
}

func TestSaveDawgFile(t *testing.T) {
	dawg := CreateDAWG([]string{"vate", "note", "vete", "vute"})
	
	err := dawg.SaveToFile("Test.dawg")
	if err != nil {
		t.Error("Saving Failed")
	}
}

func TestCreateBigDAWGfromFile(t *testing.T) {
	dawg, err := CreateDAWGFromFile("TestDawg.txt")
	if err != nil {
		t.Error("Creation From File Failed")
	}
	dawg.SaveToFile("Test.dawg")
}

func TestLoadFromFile(t *testing.T) {
	dawg, err := LoadDAWGFromFile("Test.dawg")
	if err != nil || dawg == nil {
		t.Error("Load From File Failed")
	}
}

// func TestSearchFile(t *testing.T) {
// 	files, err := SearchFile("testIndexFile.txt", "TestDawg")
// 	if err != nil {
// 		t.Error("Search Failed")
// 	}
// 	fmt.Println(files)
// }

func TestAllign(t *testing.T) {
	SCRIPT := levenshtein.EditScriptForStrings([]rune("attðəseɪmtaɪmpɒkənfɜːmmzɑːkɹɹiːdðatkɹɹaɪsttɪzvɛɹɪɡɒd"), []rune("atðəseɪmtaɪmpɔːlkənfɜːmzaʊəkɹiːdðatkɹaɪstɪzvɛɹɪɡɒd"), levenshtein.DefaultOptions)
	ScriptToAllign([]rune("attðəseɪmtaɪmpɒkənfɜːmmzɑːkɹɹiːdðatkɹɹaɪsttɪzvɛɹɪɡɒd"), []rune("atðəseɪmtaɪmpɔːlkənfɜːmzaʊəkɹiːdðatkɹaɪstɪzvɛɹɪɡɒd"), SCRIPT)
}
