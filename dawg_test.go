package dawg

import "testing"

func TestCreateDAWG(t *testing.T) {
    dawg := CreateDAWG([]string{"test", "rest", "nest", "note"})
    if (dawg.nodesCount!=8) {
        t.Error("Creation failed")
    }
}

func TestSearch(t *testing.T) {
    dawg := CreateDAWG([]string{"test", "tese", "nest", "test2", "tes", "note"})

    test := Search(dawg, "test", 0, 1, false, false)
    if (len(test)!=1 || test[0]!="test") {
        t.Error("Search failed")
    }

    test = Search(dawg, "test", 1, 10, false, false)
    if (len(test)!=3) {
        t.Error("Search failed")
    }

    test = Search(dawg, "test", 1, 10, true, true)
    if (len(test)!=5) {
        t.Error("Search failed")
    }
}
