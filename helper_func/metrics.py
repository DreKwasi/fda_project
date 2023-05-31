from helper_func import data_parser


def number_of_applicants(data):
    return data_parser.human_format(
        data["applicant"][data["applicant"] != "Not Specified"].nunique()
    )


def number_of_products(data):
    return data_parser.human_format(
        data["product_uuid"][data["product_uuid"] != "Not Specified"].nunique()
    )


def number_of_registrations(data):
    return data_parser.human_format(
        data["registration_number"][
            data["registration_number"] != "Not Specified"
        ].count()
    )


def number_of_renewals(data):
    return data_parser.human_format(
        data[data["registration_type"] == "Renewal"].shape[0]
    )
