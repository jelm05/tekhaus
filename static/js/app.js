$(document).ready(function(){

   $('table').DataTable({
      // The order parameter is an array of arrays where the first value of the inner array is the column to order on,
      // and the second is 'asc' (ascending ordering) or 'desc' (descending ordering) as required.
      // order is a 2D array to allow multi-column ordering to be defined.
      'order': [[0, 'desc']]
   });

});