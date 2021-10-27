from set import *
import pytest


"""[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 2], [0, 0, 2, 0], [0, 0, 2, 1], [0, 0, 2, 2], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 0, 2], [0, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 2], [0, 1, 2, 0], [0, 1, 2, 1], [0, 1, 2, 2], [0, 2, 0, 0], [0, 2, 0, 1], [0, 2, 0, 2], [0, 2, 1, 0], [0, 2, 1, 1], [0, 2, 1, 2], [0, 2, 2, 0], [0, 2, 2, 1], [0, 2, 2, 2], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 0, 2], [1, 0, 1, 0], [1, 0, 1, 1], [1, 0, 1, 2], [1, 0, 2, 0], [1, 0, 2, 1], [1, 0, 2, 2], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 0, 2], [1, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 2, 0], [1, 1, 2, 1], [1, 1, 2, 2], [1, 2, 0, 0], [1, 2, 0, 1], [1, 2, 0, 2], [1, 2, 1, 0], [1, 2, 1, 1], [1, 2, 1, 2], [1, 2, 2, 0], [1, 2, 2, 1], [1, 2, 2, 2], [2, 0, 0, 0], [2, 0, 0, 1], [2, 0, 0, 2], [2, 0, 1, 0], [2, 0, 1, 1], [2, 0, 1, 2], [2, 0, 2, 0], [2, 0, 2, 1], [2, 0, 2, 2], [2, 1, 0, 0], [2, 1, 0, 1], [2, 1, 0, 2], [2, 1, 1, 0], [2, 1, 1, 1], [2, 1, 1, 2], [2, 1, 2, 0], [2, 1, 2, 1], [2, 1, 2, 2], [2, 2, 0, 0], [2, 2, 0, 1], [2, 2, 0, 2], [2, 2, 1, 0], [2, 2, 1, 1], [2, 2, 1, 2], [2, 2, 2, 0], [2, 2, 2, 1], [2, 2, 2, 2]]
"""

def test_get_deck():
    deck = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 2], [0, 0, 2, 0], [0, 0, 2, 1], [0, 0, 2, 2], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 0, 2], [0, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 2], [0, 1, 2, 0], [0, 1, 2, 1], [0, 1, 2, 2], [0, 2, 0, 0], [0, 2, 0, 1], [0, 2, 0, 2], [0, 2, 1, 0], [0, 2, 1, 1], [0, 2, 1, 2], [0, 2, 2, 0], [0, 2, 2, 1], [0, 2, 2, 2], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 0, 2], [1, 0, 1, 0], [1, 0, 1, 1], [1, 0, 1, 2], [1, 0, 2, 0], [1, 0, 2, 1], [1, 0, 2, 2], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 0, 2], [1, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 2, 0], [1, 1, 2, 1], [1, 1, 2, 2], [1, 2, 0, 0], [1, 2, 0, 1], [1, 2, 0, 2], [1, 2, 1, 0], [1, 2, 1, 1], [1, 2, 1, 2], [1, 2, 2, 0], [1, 2, 2, 1], [1, 2, 2, 2], [2, 0, 0, 0], [2, 0, 0, 1], [2, 0, 0, 2], [2, 0, 1, 0], [2, 0, 1, 1], [2, 0, 1, 2], [2, 0, 2, 0], [2, 0, 2, 1], [2, 0, 2, 2], [2, 1, 0, 0], [2, 1, 0, 1], [2, 1, 0, 2], [2, 1, 1, 0], [2, 1, 1, 1], [2, 1, 1, 2], [2, 1, 2, 0], [2, 1, 2, 1], [2, 1, 2, 2], [2, 2, 0, 0], [2, 2, 0, 1], [2, 2, 0, 2], [2, 2, 1, 0], [2, 2, 1, 1], [2, 2, 1, 2], [2, 2, 2, 0], [2, 2, 2, 1], [2, 2, 2, 2]]
    my_deck = get_deck()
    assert deck == my_deck

#90 width of card; 140-height of card; 10-space between cards; 20 padding
def test_search_coordinate():
    assert search_coordinate(0, 0) == (0,0)
    assert search_coordinate(50, 60) == (1,1)
    assert search_coordinate(30, 315) == (1,0)
    assert search_coordinate(170, 10) == (2,0)
    assert search_coordinate(150, 400) == (2,3)
    assert search_coordinate(203, 80) == (2,1)
    assert search_coordinate(300, 600) == (3,0)
    assert search_coordinate(1000, 1000) == (0,0)
    assert search_coordinate(-10, 400) == (0,3)
    assert search_coordinate(15, 302) == (0,2)
    assert search_coordinate(85, 103) == (1,1)
    assert search_coordinate(300, 302) == (3,2)
    assert search_coordinate(320, 405) == (4,3)

def test_check_values_of_card():
    assert check_values_of_card(0,0,0) == True
    assert check_values_of_card(1,1,1) == True
    assert check_values_of_card(2,2,2) == True
    assert check_values_of_card(1,2,3) == True
    assert check_values_of_card(1,3,2) == True
    assert check_values_of_card(2,1,3) == True
    assert check_values_of_card(2,3,1) == True
    assert check_values_of_card(3,2,1) == True
    assert check_values_of_card(3,1,2) == True
    assert check_values_of_card(1,0,1) == False
    assert check_values_of_card(0,0,1) == False
    assert check_values_of_card(1,2,2) == False
    assert check_values_of_card(0,0,2) == False
    assert check_values_of_card(1,2,2) == False
    assert check_values_of_card(0,2,2) == False
    assert check_values_of_card(0,1,1) == False
    assert check_values_of_card(2,0,2) == False


def test_get_attributes():
    COLOR = 0 #colors are ["red", "green", "purple"]
    SHAPE = 1 #shapes are ["oval", "squiggle", "diamond"]
    SHADING = 2 #shaddings are ["solid", "striped", "outlined"]
    NUMBER = 3 #numbers are ["1", "2", "3"]
    assert get_attributes([0,0,0, 0]) == {"color": "red", "shape": "oval", "shadding": "solid", "number": 1}
    assert get_attributes([2,0,1, 2]) == {"color": "purple", "shape": "oval", "shadding": "striped", "number": 3}
    assert get_attributes([0,2,0, 2]) == {"color": "red", "shape": "diamond", "shadding": "solid", "number": 3}
    assert get_attributes([1,1,1, 1]) == {"color": "green", "shape": "squiggle", "shadding": "striped", "number": 2}
    assert get_attributes([2,1,2, 0]) == {"color": "purple", "shape": "squiggle", "shadding": "outlined", "number": 1}
    assert get_attributes([0,2,2, 1]) == {"color": "red", "shape": "diamond", "shadding": "outlined", "number": 2}
    assert get_attributes([2,0,0, 2]) == {"color": "purple", "shape": "oval", "shadding": "solid", "number": 3}
    assert get_attributes([2,2,1, 0]) == {"color": "purple", "shape": "diamond", "shadding": "striped", "number": 1}
    assert get_attributes([1,2,2, 1]) == {"color": "green", "shape": "diamond", "shadding": "outlined", "number": 2}
    assert get_attributes([1,1,0, 2]) == {"color": "green", "shape": "squiggle", "shadding": "solid", "number": 3}
    assert get_attributes([0,0,1, 0]) == {"color": "red", "shape": "oval", "shadding": "striped", "number": 1}
    

def test_get_card_canvas_area():
    assert get_card_canvas_area(1, 1) == (20, 20)
    assert get_card_canvas_area(1, 2) == (120, 20)
    assert get_card_canvas_area(1, 3) == (220, 20)
    assert get_card_canvas_area(1, 4) == (320, 20)
    assert get_card_canvas_area(2, 1) == (20, 170)
    assert get_card_canvas_area(2, 2) == (120, 170)
    assert get_card_canvas_area(2, 3) == (220, 170)
    assert get_card_canvas_area(2, 4) == (320, 170)
    assert get_card_canvas_area(3, 1) == (20, 320)
    assert get_card_canvas_area(3, 2) == (120, 320)
    assert get_card_canvas_area(3, 3) == (220, 320)
    assert get_card_canvas_area(3, 4) == (320, 320)

def test_get_position_for_shapes():
    assert get_position_for_shapes(20, 20,1) == [[35, 75]]
    assert get_position_for_shapes(220, 20,3) == [[235, 35], [235, 75], [235, 115]]
    assert get_position_for_shapes(320, 20,3) == [[335, 35], [335, 75], [335, 115]]
    assert get_position_for_shapes(20, 170,3) == [[35, 185], [35, 225], [35, 265]]
    assert get_position_for_shapes(120, 170,1) == [[135, 225]]
    assert get_position_for_shapes(220, 170,3) == [[235, 185], [235, 225], [235, 265]]
    assert get_position_for_shapes(320, 170,1) == [[335, 225]]
    assert get_position_for_shapes(20, 320,2) == [[35, 355], [35, 395]]
    assert get_position_for_shapes(120, 320,2) == [[135, 355], [135, 395]]
    assert get_position_for_shapes(220, 320,1) == [[235, 375]]
    assert get_position_for_shapes(320, 320,2) == [[335, 355], [335, 395]]

pytest.main(["-v", "--tb=line", "-rN", "set_test.py"])