$('.sol-popup').popup();
$('.ui.sticky').sticky({context: '#main-column'});
$('.ui.dropdown').dropdown({"on": "hover"});

// Quick search code for Isotope

var qsRegex;

var $grid = $('.ui.divided.items').isotope({
  itemSelector: '.element-item',
  layoutMode: 'vertical',
});

var $quicksearch = $('.quicksearch').keyup( debounce( function() {
  qsRegex = new RegExp( $quicksearch.val(), 'gi' );
  $grid.isotope({filter: function() {
    return qsRegex ? $(this).find('.header').text().match( qsRegex ) : true;
  }});
}, 200 ) );

function debounce( fn, threshold ) {
  var timeout;
  return function debounced() {
    if ( timeout ) {
      clearTimeout( timeout );
    }
    function delayed() {
      fn();
      timeout = null;
    }
    timeout = setTimeout( delayed, threshold || 100 );
  }
}

$('.clear-button').on('click', function(){
  $('.quicksearch').val('');
  $('.sol-filter').removeClass('active');
  $grid.isotope({filter: '*'});
});

$('.sol-filter').on('click', function() {
  $('.sol-filter').removeClass('active');
  $(this).addClass('active');
  var filterValue = $(this).attr('data-filter');
  $grid.isotope({ filter: filterValue });
});