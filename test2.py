


def test_dict():
    me = {
        "first": "Sebastian",
        "last": "Ruiz",
        "age": 21,
        "hobbies": [],
        "address": {
            "street": "Helix",
            "city": "San Diego"
        },
        "another": 1,
    }

    print(me["first"] + " " + me["last"])

    print("My age is: " + str(me["age"]))
    print(f"My age is: {me['age']}")

    address = me["address"]
    print(type(address))
    print(address["street"])

    print(me["address"]["city"])

    # add new key
    me["color"] = "black"

    # modify existing heys
    me["age"] = 99

    # check if a key exist in a dict
    if "age" in me:
        print("Age exists")



print("---- Dictionary Test ----")

test_dict()