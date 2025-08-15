def get_query_parser(api):
    parser = api.parser()
    parser.add_argument(
        "sort_field",
        type=str,
        help="Name of the field to sort on",
        location="args",
        required=False,
        trim=True,
    )

    parser.add_argument(
        "sort_order",
        type=str,
        help="Sort order for sort_field",
        location="args",
        required=False,
        trim=True,
        choices=["ASC", "DESC"],
    )

    parser.add_argument(
        "query",
        type=str,
        help="JSON object containing query constraints, see above for examples. No query returns all records",
        location="args",
        required=False,
        trim=True,
    )

    return parser
