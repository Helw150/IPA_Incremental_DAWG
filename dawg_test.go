package dawg

import "testing"

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
	if err != nil || !(test.final) || test.keywords == nil {
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
	if err != nil || dawg.initialState.keywords == nil {
		t.Error("Creation From File Failed")
	}
	dawg.SaveToFile("Test.dawg")
}

func TestLoadFromFile(t *testing.T) {
	dawg, err := LoadDAWGFromFile("TestDawg.txt")
	if err != nil || dawg.initialState.keywords == nil {
		t.Error("Load From File Failed")
	}
}
