try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from base_test_case import BaseTestCase, ThreadedReturnGetter
from cursesmenu import CursesMenu
from cursesmenu import SelectionMenu


class TestSelectionMenu(BaseTestCase):
    def test_select(self):
        selection_menu = SelectionMenu(strings=["a", "b", "c"], title="Select a letter")
        selection_menu.start()
        selection_menu.wait_for_start(timeout=10)
        selection_menu.go_down()
        selection_menu.select()
        selection_menu.join(timeout=10)
        self.assertFalse(selection_menu.is_alive())
        self.assertEqual(selection_menu.selected_option, 1)

    def test_get_selection(self):
        menu = []
        menu_thread = ThreadedReturnGetter(SelectionMenu.get_selection, args=[["One", "Two", "Three"]],
                                           kwargs={"_menu": menu})

        menu_thread.start()
        while not menu:
            continue
        menu = menu[0]
        menu.wait_for_start(timeout=10)
        menu.go_down()
        menu.select()
        print(menu.returned_value)
        menu_thread.join(timeout=10)
        self.assertFalse(menu_thread.is_alive())
        self.assertEqual(menu_thread.return_value, 1)

    def test_current_menu(self):
        menu = []
        self.menu_thread = ThreadedReturnGetter(SelectionMenu.get_selection, args=[["One", "Two", "Three"]],
                                                kwargs={"_menu": menu})

        self.menu_thread.start()
        while not menu:
            continue
        menu = menu[0]
        menu.wait_for_start(timeout=10)
        self.assertIsInstance(CursesMenu.currently_active_menu, SelectionMenu)
        self.assertIs(CursesMenu.currently_active_menu, menu)

        selection_menu = SelectionMenu(strings=["a", "b", "c"], title="Select a letter")
        selection_menu.start()
        selection_menu.wait_for_start(timeout=10)
        self.assertIs(CursesMenu.currently_active_menu, selection_menu)

    def test_init(self):
        selection_menu_1 = SelectionMenu(["1", "2", "3"])
        selection_menu_2 = SelectionMenu(["4", "5"], "selection_menu_2", "test_init", True)
        selection_menu_3 = SelectionMenu(strings=["6", "7", "8", "9"], title="selection_menu_3", subtitle="test_init",
                                         show_exit_option=False)
        self.assertIsNone(selection_menu_1.title)
        self.assertEqual(selection_menu_2.title, "selection_menu_2")
        self.assertEqual(selection_menu_3.title, "selection_menu_3")
        self.assertIsNone(selection_menu_1.subtitle)
        self.assertEqual(selection_menu_2.subtitle, "test_init")
        self.assertEqual(selection_menu_3.subtitle, "test_init")
        self.assertTrue(selection_menu_1.show_exit_option)
        self.assertTrue(selection_menu_2.show_exit_option)
        self.assertFalse(selection_menu_3.show_exit_option)
        self.assertEqual(selection_menu_1.items[1].text, "2")
        self.assertEqual(selection_menu_2.items[0].text, "4")
        self.assertEqual(selection_menu_3.items[3].text, "9")
