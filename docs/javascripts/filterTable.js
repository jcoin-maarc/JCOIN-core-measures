function filterTables() {
    // Get the search input value
    var input = document.getElementById("searchInput").value;
    // Get all the table rows
    var rows = document.getElementsByTagName("tr");
    // Loop through all the rows
    for (var i = 0; i < rows.length; i++) {
      var td = rows[i].getElementsByTagName("td");
      // Check if any of the table cells contain the search input value
      for (var j = 0; j < td.length; j++) {
        if (td[j].innerHTML.indexOf(input) > -1) {
          // If a match is found, set the row's display to "table-row"
          rows[i].style.display = "table-row";
          break;
        } else {
          // If no match is found, set the row's display to "none"
          rows[i].style.display = "none";
        }
      }
    }
  }