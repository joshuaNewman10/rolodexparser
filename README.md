                          Rolodex Parser

  What is it?
  -----------

  The Rolodex Parser is a module that takes in user information in any of 
  the following formats: 

  Lastname, Firstname, (703)-742-0996, Blue, 10013 
  Firstname Lastname, Red, 11237, 703 955 0373 
  Firstname, Lastname, 10013, 646 111 0101, Green

  and parses out this data into a JSON object in the following format:


  {
    "entries": [
    {
      "color": "yellow",
      "firstname": "James",
      "lastname": "Murphy", 
      "phonenumber": "018-154-6474", 
      "zipcode": "83880"
    }, {
      "color": "yellow",
      "firstname": "Booker T.", 
      "lastname": "Washington", 
      "phonenumber": "373-781-7380", 
      "zipcode": "87360"
    } 
    ],
    "errors": [
      1,
      3
    ]
  }

  Usage
  ------------

  The RolodexParser module can be used by running the following command 
  from the terminal:

  python rolodex_parser.py input_file_name output.json

  Unit tests can be run via the following command:

  python unit_tests.py


  Contacts
  --------

     o Please send all comments to jonewman1020@gmail.com

     
