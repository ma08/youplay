from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class TestSampleMenu(BaseTestCase):
    def setUp(self):
        super(TestSampleMenu, self).setUp()

        self.menu = CursesMenu("self.menu", "TestSampleMenu")
        self.item1 = MenuItem("self.item1", self.menu)
        self.item2 = MenuItem("self.item2", self.menu)
        self.menu.append_item(self.item1)
        self.menu.append_item(self.item2)
        self.menu.start()
        self.menu.wait_for_start(timeout=10)

    def tearDown(self):
        super(TestSampleMenu, self).tearDown()
        self.menu.exit()
        self.menu.join(timeout=10)

    def test_go_down(self):
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 1)
        self.assertIs(self.menu.current_item, self.item2)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 2)
        self.assertEqual(self.menu.current_item, self.menu.exit_item)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)

    def test_go_up(self):
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 2)
        self.assertIs(self.menu.current_item, self.menu.exit_item)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 1)
        self.assertEqual(self.menu.current_item, self.item2)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)

    def test_go_to(self):
        self.menu.go_to(1)
        self.assertEqual(self.menu.current_option, 1)
        self.assertEqual(self.menu.current_item, self.item2)

    def test_select(self):
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 0)
        self.assertIs(self.menu.selected_item, self.item1)
        self.menu.go_down()
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 1)
        self.assertIs(self.menu.selected_item, self.item2)
        self.menu.go_down()
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 2)
        self.assertIs(self.menu.selected_item, self.menu.exit_item)
        self.menu.join(timeout=10)
        self.assertFalse(self.menu.is_alive())

    def test_exit(self):
        self.menu.exit()
        self.menu.join(timeout=10)
        self.assertFalse(self.menu.is_alive())


class TestCursesMenu(BaseTestCase):
    def test_init(self):
        menu1 = CursesMenu()
        menu2 = CursesMenu("menu2", "test_init", True)
        menu3 = CursesMenu(title="menu3", subtitle="test_init", show_exit_option=False)
        self.assertIsNone(menu1.title)
        self.assertEqual(menu2.title, "menu2")
        self.assertEqual(menu3.title, "menu3")
        self.assertIsNone(menu1.subtitle)
        self.assertEqual(menu2.subtitle, "test_init")
        self.assertEqual(menu3.subtitle, "test_init")
        self.assertTrue(menu1.show_exit_option)
        self.assertTrue(menu2.show_exit_option)
        self.assertFalse(menu3.show_exit_option)

    def test_currently_active_menu(self):
        menu1 = CursesMenu("menu1", "test_currently_active_menu")
        menu2 = CursesMenu("menu2", "test_currently_active_menu")
        self.assertIsNone(CursesMenu.currently_active_menu)
        menu1.start()
        menu1.wait_for_start(10)
        self.assertIs(CursesMenu.currently_active_menu, menu1)
        menu2.start()
        menu2.wait_for_start(10)
        self.assertIs(CursesMenu.currently_active_menu, menu2)
