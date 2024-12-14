[![Downloads](https://static.pepy.tech/personalized-badge/django-query-to-table?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/django-query-to-table)

### django-query-to-table (DjangoQtt) is an easy to use django package to generate html table from sql query.

You can read more about this package here : [django query to table package](https://mshaeri.com/blog/generate-html-table-report-from-sql-query-in-django/)

The package contains one function named "generateFromSql" accepting 12 arguments :

* cursor : DB cursor
* title : The title of the report that will be shown on top of table
* sqltext : The sql select query to retrieve data
* footerCols : A list of columns name that you want to have Sum of values on footer . Example : ['amount','price']
* htmlClass : Html CSS classes for the table
* direction (default = "ltr") : Indicates direction of the report page.  "ltr"- Left to Right , "rtl" -  Right to Left
* font (default = "Tahoma") : Font of title and table contents
* totalText (default = "Total") : Title of footer row that will be the put below the first column.
* rowIndex (default = False) : Indicates whether the table should have index column or not.
* headerRowColor (default = '#eeeeee') :  The header (title) row background color.
* evenRowColor (default = '#ffffff') :  The even rows background color.
* oddRowColor (default = '#ffffff') :  The odd rows background color.



## Installation
Run following command to install DjangoQtt :

```shell
pip install django-query-to-table
```

## Usage :

- Generate html table by SQL query
```python
from django.db import connection
from django_query_to_table import DjangoQtt
from django.http import HttpResponse

# view function in Django project
def listOfPersons(request):
  reportTitle = "Employee List"
  sqlQuery = "SELECT FirstName as 'First Name', LastName as 'Last Name', phone as 'Phone Number', salary as 'Salary' FROM persons"
  columnsToBeSummarized = ['Salary']
  fontName = "Arial"
  cssClasses = "reportTable container"
  headerRowBackgroundColor = '#ffeeee'
  evenRowsBackgroundColor = '#ffeeff'
  oddRowsBackgroundColor = '#ffffff'
  rowIndexVisibility = True
  table = DjangoQtt.generate_from_sql(reportTitle, sqlQuery, columnsToBeSummarized, cssClasses,
                                  "ltr", fontName, "Total Salary", rowIndexVisibility,
                                  headerRowBackgroundColor, evenRowsBackgroundColor, oddRowsBackgroundColor
                                  )
  
  # here the table is a string variable contianing the html table showing the query result
  return HttpResponse(table)
   
 ```

