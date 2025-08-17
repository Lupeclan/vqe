spaceship_singular_model = """
{
    \"model\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"Stardust Seeker\"
            }
        ]
    }
}
"""

spaceship_two_models = """
{
    \"model\": {
        \"operator\": \"or\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"Nebula Rider\"
            },
            {
                \"operator\": \"equals\",
                \"value\": \"Stardust Seeker\"
            }
        ]
    }
}
"""

spaceship_manufacturer_and_year = """
{
    \"manufacturer\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"AetherForge\"
            }
        ]
    },
    \"year\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"gt\",
                \"value\": 2010
            }
        ]
    }
}
"""

car_less_than_or_equal_seats = """
{
    \"seats\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"lte\",
                \"value\": 7
            }
        ]
    }
}
"""

car_colours = """
{
    \"colour\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"startsWith\",
                \"value\": \"Light\"
            },
            {
                \"operator\": \"contains\",
                \"value\": \"Y\"
            }
        ]
    }
}
"""

car_make_and_year = """
{
    \"make\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"endsWith\",
                \"value\": \"s\"
            }
        ]
    },
    \"year\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"in\",
                \"value\": [
                    1971,
                    2002
                ]
            }
        ]
    }
}
"""

bike_gears_and_type_and_year = """
{
    \"gears\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"gt\",
                \"value\": 3
            }
        ]
    },
    \"type\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"notIn\",
                \"value\": [
                    "BMX",
                    "Road"
                ]
            }
        ]
    },
    \"year\": {
        \"operator\": \"or\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": 2023
            },
            {
                \"operator\": \"equals\",
                \"value\": 2014
            }
        ]
    }
}
"""