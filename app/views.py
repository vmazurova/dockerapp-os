import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, Child, Tool

def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ["name", "personal_celphone", "birthday", "contact_group.name", "tool.name"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                    "tool"
                ],
                "expanded": False,
            },
        ),
        (
            "Other",
            {
                "fields": [
                    "tool",
                    ],
                "expanded": False,
                }
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                ],
                "expanded": False,
            },
        ),
        (

            "Other",
            {
                "fields": [
                    "tool",
                    ],
                "expanded": False,
                }
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                ],
                "expanded": False,
            },
        ),
        (
            "Other",
            {
                "fields": [
                    "tool",
                    ],
                "expanded": False,
                }

        ),
    ]

class ChildModelView(ModelView):
    datamodel = SQLAInterface(Child)

    list_columns = ["name", "birthday",  "parent"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "parent",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "parent",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "parent",
                ],
                "expanded": False,
            },
        ),
    ]

class ToolModelView(ModelView):
    datamodel = SQLAInterface(Tool)

    list_columns = ["name",  "description"]

    base_order = ("id", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name", "description" ]}),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "description"]}),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "description" ]}),
    ]
class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = "Grouped Birth contacts"
    chart_type = "AreaChart"
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "year",
            "formatter": pretty_year,
            "series": [(aggregate_count, "group")],
        },
    ]


db.create_all()
fill_gender()
appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)
appbuilder.add_view(
    ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts"
)
appbuilder.add_view(
    ChildModelView, "List Children", icon="fa-child", category="Contacts"
)
appbuilder.add_view(
    ToolModelView, "List Tools", icon="fa-toolbox", category="Contacts"
)
appbuilder.add_separator("Contacts")
appbuilder.add_view(
    ContactTimeChartView,
    "Contacts Birth Chart",
    icon="fa-dashboard",
    category="Contacts",
)

