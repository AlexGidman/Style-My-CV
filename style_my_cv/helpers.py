"""
Helper functions for style_my_cv flask application
"""

def fmonth(month):
    """Returns month as short-hand from numerical input"""
    if month == 1:
        return "Jan"
    if month == 2:
        return "Feb"
    if month == 3:
        return "Mar"
    if month == 4:
        return "April"
    if month == 5:
        return "May"
    if month == 6:
        return "June"
    if month == 7:
        return "July"
    if month == 8:
        return "Aug"
    if month == 9:
        return "Sept"
    if month == 10:
        return "Oct"
    if month == 11:
        return "Nov"
    if month == 12:
        return "Dec"
    else:
        raise ValueError("Must be integer between 1 & 12)")

def convert_to_dict(fetchone) -> dict:
    return dict(fetchone) if fetchone else None

def convert_to_list_of_dicts(fetchall: iter=None) -> list:
    """Converts sqlite3.Cursor object from 'fetchall' to a list of dicts"""
    return [dict(row) for row in fetchall]

def cv_date_format(cv_entries: list):
    """Directly modifies the format of 'datestart' & 'dateend' key-values for each dict in list
    
    Typical Usage Example: 
        As datestart and dateend stored in db as numerical values for sorting order, they must be formatted
        for using on CV.

        print(employment[0]['datestart'])
        '1997-09'

        cv_date_format(employment)

        print(employment[0]['datestart'])
        'Sept 1997'
    
    Args:
        cv_entries(list): list of dicts that represent rows from the database. Each dict must contain 'datestart' 
          and 'dateend' keys.
    
    Raises:
        KeyError: No 'datestart' key found
        KeyError: No 'dateend' key found
    """
    
    for entry in cv_entries:
        try:
            x = int(entry['datestart'][5:8])
            entry['datestart'] = f"{fmonth(x)} {entry['datestart'][:4]}"
        except KeyError:
            raise KeyError("No 'datestart' key found")
        
        try:
            if entry['dateend'] == 'Present':
                entry['dateend'] = 'Present'
            else:
                y = int(entry['dateend'][5:8])
                entry['dateend'] = f"{fmonth(x)} {entry['dateend'][:4]}"
        except KeyError:
            raise KeyError("No 'dateend' key found")
