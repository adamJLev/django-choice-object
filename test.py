import unittest

from django_choice_object import Choice


class TestChoice(Choice):
    FIRST = 1, "zed"
    SECOND = 2
    THIRD = 3
    FOURTH = 4, "a description"
    WITH_UNDERSCORE = 5
    MORE_VALUES = 6, "another description"


class TestChoiceInheritance(TestChoice):
    EXTRA_VALUE = 7


class TestChoiceOrdered(TestChoice):
    ZED = 7, "zzzzzzzzz"
    _order_by = "name"


class TestCustomOrdering(Choice):
    LAST = ('last', 'Last', 10)
    FIRST = ('first', 'First', 1)

    @staticmethod
    def _get_sort_key(value):
        return value[2]


class TestCustomOrderingInheritance(TestCustomOrdering):
    MIDDLE = ('middle', 'Middle', 5)


class TestSimple(Choice):
    OTHER = 10


class TestMultipleInheritance(TestChoice, TestSimple):
    pass


class TestGroups(Choice):
    FIRST = 0
    MIDDLE = 1
    LAST = 2
    EXTRA_LAST = 3

    STARTED_GROUP = set((FIRST, MIDDLE))
    END_GROUP = set((LAST, EXTRA_LAST))


class TestGroupsWithNames(Choice):
    FIRST = 1, "abc"
    SECOND = 2, "abc"
    THIRD = 3, "abc"

    A_GROUP = set((FIRST, SECOND, THIRD))


def get_name_from_choices(value, choices):
    for id, name in choices:
        if id == value:
            return name


class TestChoices(unittest.TestCase):
    def testInstance(self):
        self.assertEqual(list(TestChoice()), list(TestChoice))
        self.assertEqual(list(TestChoiceOrdered()), list(TestChoiceOrdered))
        self.assertEqual(list(TestChoiceInheritance()), list(TestChoiceInheritance))

    def testInheritance(self):
        self.assertEqual(list(TestChoiceInheritance)[:-1], list(TestChoice))

    def testNames(self):
        fourth_name = get_name_from_choices(TestChoice.FOURTH, list(TestChoice))
        self.assertEqual(fourth_name, "a description")

        underscore_name = get_name_from_choices(TestChoice.WITH_UNDERSCORE, list(TestChoice))
        self.assertEqual(underscore_name, "With Underscore")

        self.assertEqual(TestChoice.get_by_name("a description"), TestChoice.FOURTH)
        self.assertEqual(TestChoice.get_by_value(TestChoice.FOURTH), fourth_name)

    def testOrderBy(self):
        self.assertNotEqual(list(TestChoice), list(TestChoiceOrdered))
        self.assertTrue(list(TestChoiceOrdered)[-1][0] == TestChoiceOrdered.ZED)
        self.assertEqual(list(TestChoice)[0][0], TestChoice.FIRST)

    def testCustomOrdering(self):
        self.assertEqual(list(TestCustomOrdering)[0][0], TestCustomOrdering.FIRST)
        self.assertEqual(list(TestCustomOrdering)[-1][0], TestCustomOrdering.LAST)
        self.assertEqual(list(TestCustomOrderingInheritance)[0][0], TestCustomOrdering.FIRST)
        self.assertEqual(list(TestCustomOrderingInheritance)[-1][0], TestCustomOrdering.LAST)

    def testMultipleInheritance(self):
        self.assertEqual(list(TestMultipleInheritance), list(TestChoice) + list(TestSimple))

    def testGroups(self):
        self.assertEqual(len(list(TestGroups)), 4)
        self.assertTrue(isinstance(TestGroups.STARTED_GROUP, set))
        self.assertTrue(isinstance(TestGroups.END_GROUP, set))

    def testGroupsWithNames(self):
        self.assertEqual(TestGroupsWithNames.A_GROUP, set((1, 2, 3)))


if __name__ == "__main__":
    unittest.main()
