from ..v1.users.control import UserControl

user_control = UserControl()

if __name__ == "__main__":
    user_control = UserControl()


user_data = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "user_name": "john_doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "user_name": "jane_smith",
        "email": "jane.smith@example.com",
        "password": "securepass456",
        "is_active": True,
        "role": "admin"
    },
    {
        "first_name": "Robert",
        "last_name": "Johnson",
        "user_name": "robert_j",
        "email": "robert.johnson@example.com",
        "password": "robertpass789",
        "is_active": False,
        "role": "mechanic"
    },
    {
        "first_name": "Alice",
        "last_name": "Brown",
        "user_name": "alice_b",
        "email": "alice.brown@example.com",
        "password": "alicepass101",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "Michael",
        "last_name": "Williams",
        "user_name": "mike_w",
        "email": "mike.williams@example.com",
        "password": "michael1234",
        "is_active": True,
        "role": "mechanic"
    },
    {
        "first_name": "Emily",
        "last_name": "Jones",
        "user_name": "emily_j",
        "email": "emily.jones@example.com",
        "password": "emilypass2022",
        "is_active": True,
        "role": "admin"
    },
    {
        "first_name": "Chris",
        "last_name": "Taylor",
        "user_name": "chris_t",
        "email": "chris.taylor@example.com",
        "password": "christaylor78",
        "is_active": False,
        "role": "customer"
    },
    {
        "first_name": "Laura",
        "last_name": "Davis",
        "user_name": "laura_d",
        "email": "laura.davis@example.com",
        "password": "laurapass55",
        "is_active": True,
        "role": "mechanic"
    },
    {
        "first_name": "Daniel",
        "last_name": "Martinez",
        "user_name": "dan_m",
        "email": "daniel.martinez@example.com",
        "password": "danielsecure",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "Sophia",
        "last_name": "Anderson",
        "user_name": "sophia_a",
        "email": "sophia.anderson@example.com",
        "password": "sophiapass",
        "is_active": True,
        "role": "admin"
    },
    {
        "first_name": "James",
        "last_name": "Lee",
        "user_name": "james_l",
        "email": "james.lee@example.com",
        "password": "leejamespw",
        "is_active": False,
        "role": "mechanic"
    },
    {
        "first_name": "Olivia",
        "last_name": "Garcia",
        "user_name": "olivia_g",
        "email": "olivia.garcia@example.com",
        "password": "oliviasecure",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "David",
        "last_name": "Hernandez",
        "user_name": "david_h",
        "email": "david.hernandez@example.com",
        "password": "davidpw123",
        "is_active": True,
        "role": "admin"
    },
    {
        "first_name": "Emma",
        "last_name": "Lopez",
        "user_name": "emma_l",
        "email": "emma.lopez@example.com",
        "password": "emmapass456",
        "is_active": False,
        "role": "customer"
    },
    {
        "first_name": "Liam",
        "last_name": "Gonzalez",
        "user_name": "liam_g",
        "email": "liam.gonzalez@example.com",
        "password": "liamsecurepw",
        "is_active": True,
        "role": "mechanic"
    },
    {
        "first_name": "Isabella",
        "last_name": "Clark",
        "user_name": "isabella_c",
        "email": "isabella.clark@example.com",
        "password": "isabellapw",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "Ethan",
        "last_name": "Lewis",
        "user_name": "ethan_l",
        "email": "ethan.lewis@example.com",
        "password": "ethansecure",
        "is_active": True,
        "role": "admin"
    },
    {
        "first_name": "Mia",
        "last_name": "Robinson",
        "user_name": "mia_r",
        "email": "mia.robinson@example.com",
        "password": "miapw321",
        "is_active": False,
        "role": "mechanic"
    },
    {
        "first_name": "Noah",
        "last_name": "Walker",
        "user_name": "noah_w",
        "email": "noah.walker@example.com",
        "password": "noahsecure123",
        "is_active": True,
        "role": "customer"
    },
    {
        "first_name": "Ava",
        "last_name": "Young",
        "user_name": "ava_y",
        "email": "ava.young@example.com",
        "password": "avapass2021",
        "is_active": True,
        "role": "admin"
    }
]


try:
    new_user = user_control.add_user(**user_data)
    print(f"User added successfully: {new_user.to_dict()}")
except Exception as e:
    print(f"Error adding user: {e}")