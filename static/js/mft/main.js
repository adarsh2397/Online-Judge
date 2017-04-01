$(document).ready(function(){
    $('#page-heading').delay(1000).slideDown('slow');
    $('#input-data-form').delay(1000).fadeIn('slow');


    $('#next-button').click(function(){
        $(this).fadeOut('slow');
        console.log('Hello');
        var noOfBlocks = $('#no_of_blocks_input').val();
        $('#part-2').append('<h4>Enter the following block sizes:</h4>');
        for(var i=1;i<=noOfBlocks;i++){
            $('#part-2').append('<div class="form-group" id="block_size_inputs">' +
                '<label class="control-label col-sm-4" for="block_size_'+ i +'">Block '+ i +':</label>' +
                '<div class="col-sm-8">' +
                    '<input type="number" class="form-control" name="block_size_'+ i +'" id="block_size_input" placeholder="Enter Size" required  min="1" style="1/">' +
                '</div>' +
            '</div>');
        }
        function temp(){
            $('#part-2').delay(1000).slideDown('slow');
            $('#submit-button').delay(1000).fadeIn('slow');
        }

        temp();
    });

});