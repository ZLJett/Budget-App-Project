# put help statment here

class Category:
  def __init__(self, category_name):
    self.category_name = category_name
    self.ledger = []

  def deposit(self, amount, description = ""):
    deposit_entry = {"amount": amount, "description": description}
    self.ledger.append(deposit_entry)

  def get_balance(self):
    category_balance = 0
    # total all entries in the ledger 
    for entry in self.ledger:
      category_balance += entry["amount"]
    return category_balance

  def check_funds(self, amount):
    current_balance = self.get_balance()
    if amount > current_balance:
      return False
    else:
      return True

  def withdraw(self, amount, description = ""):
    # check if not enough funds for withdrawal 
    if not self.check_funds(amount):
      return False
    # convert entered amount into a negative amount 
    negative_amount = -amount
    # enter the withdrawal and its discription into ledger 
    withdrawal_entry = {"amount": negative_amount, "description": description}
    self.ledger.append(withdrawal_entry)
    return True
    
  def transfer(self, amount, category):
    # check if not enough funds for withdrawal 
    if not self.check_funds(amount):
      return False
    # automatically create description for withdrawal from this category
    withdrawal_description = "Transfer to " + category.category_name
    self.withdraw(amount, withdrawal_description)
    # automatically create description for deposit into destination category
    deposit_description = "Transfer from " + self.category_name
    category.deposit(amount, deposit_description)
    return True

  def __str__(self):
    # setup first row: title line formating 
    title_line_spacing = "{:*^" + str(30)+ "}"
    title_line = title_line_spacing.format(self.category_name)
    
    # setup formating for each ledger entry row
    ledger_line_spacing = "{:23.23}" + "{:>7.7}" 

    # setup final row: total balance formating
    total_balance_line = "Total: " + str(self.get_balance())
    
    # put order rows and fill in information for ledger entry rows
    ledger_rows = []
    ledger_rows.append(title_line)
    for entry in self.ledger:
      entry_amount_to_currency = "{:.2f}".format(entry["amount"])
      ledger_entry_line = ledger_line_spacing.format(entry["description"], entry_amount_to_currency)
      ledger_rows.append(ledger_entry_line)
    ledger_rows.append(total_balance_line)
    
    # stack rows into final output 
    ledger_printout = "\n".join(ledger_rows)
    return ledger_printout 




def create_spend_chart(categories):
  number_of_columns = len(categories)
  chart_body = []
  
  # find percentage spent (i.e. each categories’ percentage of total withdrawals) and return as rounded down single digit (i.e. 70% = 7)
  # return format: [{"name": "Food", "percentage": 6}, {"name": "Clothing", "percentage": 2}, {"name": "Auto", "percentage": 1}]
  category_data = process_category_data(categories)

  # returns a list of template rows
  chart_template = create_chart_template(number_of_columns)

  # takes the category percentages and converts them into the bar chart data as a list of rows
  chart_content = create_chart_content(category_data)

  # creates bottom of chart, namely the names of each category displayed vertically, as a list of each row as a string
  chart_labels = create_chart_labels(category_data)
  
  # merge chart template and content into a list of string, each string being a row of the final output
  for template_row, content_row in zip(chart_template, chart_content):
    completed_row = template_row.format(*content_row)
    chart_body.append(completed_row)
  
  # bring all pieces of chart together and convert into one large string 
  first_row = "Percentage spent by category"
  full_chart_as_list = chart_body + chart_labels
  completed_chart = first_row + "\n" + "\n".join(full_chart_as_list)
  return completed_chart


# creates a list of dictionaries, each containing one category object's name and percent spent (rounded to single digit)
def process_category_data(list_of_categories):
  total_withdrawals = 0 # this is the combined total from all categories 
  withdrawals_by_category = [] # this is a list of dictionaries each of a category's name and it's total withdrawals
  category_percentages = [] # this is a list of dictionaries each of a category's name and it's pecentage of total withdrawals
  
  # go through each category's ledger and pull out all withdrawals (i.e. negative numbers)
  for category in list_of_categories:
    category_total = 0
    for entry in category.ledger:
      if entry["amount"] < 0:
        category_total += entry["amount"]
    category_withdrawal_data = {"name": category.category_name, "category_withdrawals": category_total}
    total_withdrawals += category_total
    withdrawals_by_category.append(category_withdrawal_data)
  
  # go through each category's total withdrawals to find out what percent the category's withdrawals are of total withdrawals from all categories
  for category in withdrawals_by_category:
    category_percent_of_total = (category["category_withdrawals"] / total_withdrawals) * 100
    # truncates to 10s place, i.e. 23.45% becomes 2, thus rounded down and only single digit
    category_percent_rounded_down = int(category_percent_of_total // 10) # int used to remove float
    category_percent_data = {"name": category["name"], "percentage": category_percent_rounded_down}
    category_percentages.append(category_percent_data)
  
  return category_percentages


# creates a chart template that is the right size for the number of columns, returning as a list of template rows strings from 100 to 0
def create_chart_template(number_of_columns):
  row_list = []
  row_percent_value = 100 # each time create a new row will attach this value 
  chart_columns = 1 + number_of_columns + (number_of_columns * 2) # one for first blank column, number of columns, plus two spaces after each column

  # create each row iterating down from 100 to 0 %
  while row_percent_value != -10:
    # pad row percent value if less than three characters to keep rows even
    if len(str(row_percent_value)) == 2:
       row_padding = " " # padding for 2 digit numbers
    elif len(str(row_percent_value)) == 1:
      row_padding = "  " # padding for 1 digit numbers, i.e. 0
    else:
      row_padding = "" # where no padding is needed
    row_string = row_padding + str(row_percent_value) + "|" + ("{}" * chart_columns)
    row_list.append(row_string)
    row_percent_value -= 10
  
  # returns list of rows to be modified individually
  return row_list


# This takes the percentage of each category and creates each row of data as a list to input into the chart template,
# at the end forming a 2D matrix corresponding to the final bar chart. 
def create_chart_content(category_percentages):
  list_of_rows = []
  row_count = 10 # row_count is starting row percent, -1 digit, i.e. 10 = 100% and 0 = 0%

  # This iterates down the rows starting at 10 (100%) and going down to 0 (0%), 
  # creating each row as a list of each column's elements, in order. 
  while row_count > -1: 
    row_list = []
    category_count = len(category_percentages)
    current_category = 0 # index of current category on list of categories
    row_list.append(" ") # this is that first empty space 
      
    # iterate through each category, adding "o" if needs to be on this row, then adding the two spaces after it
    while category_count > 0:
      # Grab value from current category and see if its percentage value belongs on this row 
      # by checking if its percent is equal or less than the percent of this row
      if category_percentages[current_category]["percentage"] >= row_count: 
        row_list.append("o")
      else:
        row_list.append(" ")
      
      # adds the two blank spaces after each category 
      row_list.append(" ") 
      row_list.append(" ")
      current_category += 1
      category_count -= 1

    # Add created row to list of rows 
    list_of_rows.append(row_list)
    # move to next row
    row_count -= 1

  # return the list of rows
  return list_of_rows


# this takes the category names and makes them vertical with the proper spacing and returns this in a list of rows (with each row being a string)
def create_chart_labels(category_names):
  list_of_rows = []
  category_count = len(category_names)
  category_names_list = [category_names[x]["name"] for x in range(len(category_names))]
  left_padding = "    " # 4 whitespace, this covers the blank space on left side of the dashes
  row_count = len(max(category_names_list, key=len)) # the number of rows I want to create

  # create first row of dashes 
  first_line = "-" * (1 + category_count + (category_count * 2)) # one for first blank column, number of columns, plus two spaces after each column
  first_row = left_padding + first_line
  list_of_rows.append(first_row)

  # construct each row
  # note here that the row count is being used as an index count, staring at
  for row in range(row_count):
    row_string = ""
    row_string += left_padding + " " # this adds padding then that first empty space  
    
    for name in category_names_list:
      try:
        row_string += (name[row]) 
      except IndexError:
        row_string += " "
      # adds the two blank spaces after each category 
      row_string += "  "
    
    # Add created row to list of rows 
    list_of_rows.append(row_string)

  # return the list of rows
  return list_of_rows

if __name__ == "__main__":
  food = Category("Food")
  food.deposit(1000, "initial deposit")
  food.withdraw(10.15, "groceries")
  food.withdraw(15.89, "restaurant and more food for dessert")
  # print(food.get_balance())
  clothing = Category("Clothing")
  food.transfer(50, clothing)
  clothing.withdraw(25.55)
  clothing.withdraw(100)
  auto = Category("Auto")
  auto.deposit(1000, "initial deposit")
  auto.withdraw(15)

  print(clothing)
  print(auto)
  print(food)
  print(create_spend_chart([food, clothing, auto]))
   