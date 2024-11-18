def setup_database(db_object):
    """Handle database setup and data import"""
    tables = ["books", "members", "students", "loan"]
    for table in tables:
        print(f"Importing data for {table}...")
        db_object.import_data(table, f"{table}.csv")
    print("Database setup complete!")

def show_unreturned_books(db_object):
    """Display all unreturned books"""
    unreturned = db_object.get_unreturned_books()
    print("\nUnreturned Books:")
    print("Title | Member Name | Borrow Date")
    print("-" * 50)
    for book in unreturned:
        print(f"{book[0]} | {book[1]} | {book[2]}")

def perform_search(db_object):
    """Handle fuzzy search functionality"""
    table = input("Which table would you like to search? (books/members/students): ")
    column = input("Which column would you like to search in? ")
    keyword = input("Enter your search keyword: ")
    
    results = db_object.fuzzy_search(table, column, keyword)
    print("\nSearch Results:")
    for result in results:
        print(result)

def show_borrow_frequency(db_object):
    """Display borrowing frequency statistics"""
    limit = input("How many results would you like to see? (press Enter for all): ")
    desc = input("Sort in descending order? (y/n): ").lower() == 'y'
    
    limit = int(limit) if limit.strip() else None
    results = db_object.borrowing_freq_by_category(desc=desc, limit=limit)
    
    print("\nBorrowing Frequency by Category and Major:")
    print("Category | Major | Frequency")
    print("-" * 50)
    for result in results:
        print(f"{result[0]} | {result[1]} | {result[2]}")

def show_recent_transactions(db_object):
    """Display recent borrowing transactions"""
    count = int(input("How many recent transactions would you like to see? "))
    transactions = db_object.recent_borrow_transactions(count)
    
    print("\nRecent Transactions:")
    print("Title | Member Name | Borrow Date")
    print("-" * 50)
    for trans in transactions:
        print(f"{trans[0]} | {trans[1]} | {trans[2]}")

def show_major_stats(db_object):
    """Display statistics by major"""
    desc = input("Sort in descending order? (y/n): ").lower() == 'y'
    stats = db_object.avg_borrows_by_major(desc=desc)
    
    print("\nBorrowing Statistics by Major:")
    print("Major | Total Students | Total Borrows | Avg Borrows/Student")
    print("-" * 70)
    for stat in stats:
        print(f"{stat[0]} | {stat[1]} | {stat[2]} | {stat[3]}")