/********* Table sorter script *************/

/*
  Sets up table sorting by clicking header cells
  for $('table.listing:not(.nosort) thead th:not(.nosort)')
*/

(function($) {

function sortable(a) {
    // convert a to something sortable
    // A number, but not a date?
    if (a.charAt(4) !== '-' && a.charAt(7) !== '-' && !isNaN(parseFloat(a))) {
        return parseFloat(a);    
    }
    return a.toLowerCase();
}

function sort() {
    var th, colnum, table, tbody, reverse, index, data, usenumbers, tsorted;

    th = $(this).closest('th');
    colnum = $('th', $(this).closest('thead')).index(th);
    table = $(this).parents('table:first');
    tbody = table.find('tbody:first');
    tsorted = parseInt(table.attr('sorted') || '-1', 10);
    reverse = tsorted === colnum;

    $(this).parent().find('th:not(.nosort) .sortdirection')
        .html('&#x2003;');
    $(this).children('.sortdirection').html(
        reverse ? '&#x25b2;' : '&#x25bc;');
    
    index = $(this).parent().children('th').index(this);
    data = [];
    usenumbers = true;
    tbody.find('tr').each(function() {
        var cells, sortableitem;

        cells = $(this).children('td');
        sortableitem = sortable(cells.slice(index,index+1).text());
        if (isNaN(sortableitem)) {usenumbers = false;}
        data.push([
            sortableitem,
            // crude way to sort by surname and name after first choice
            sortable(cells.slice(1,2).text()), sortable(cells.slice(0,1).text()),
            this]);
    });

    if (data.length) {
        if (usenumbers) {
            data.sort(function(a,b) {return a[0]-b[0];});
        } else {
            data.sort();
        }
        if (reverse) {data.reverse();}
        table.attr('sorted', reverse ? '' : colnum);

        // appending the tr nodes in sorted order will remove them from their old ordering
        tbody.append($.map(data, function(a) { return a[3]; }));
        // jquery :odd and :even are 0 based
        tbody.find('tr').removeClass('odd').removeClass('even')
            .filter(':odd').addClass('even').end()
            .filter(':even').addClass('odd');
    }    
}

$(function() {
    // set up blank spaceholder gif
    var blankarrow = $('<span>&#x2003;</span>').addClass('sortdirection');
    // all listing tables not explicitly nosort, all sortable th cells
    // give them a pointer cursor and  blank cell and click event handler
    // the first one of the cells gets a up arrow instead.
    $('table.listing:not(.nosort) thead th:not(.nosort)')
        .append(blankarrow.clone())
        .css('cursor', 'pointer')
        .click(sort);

    
});

})(jQuery);
