$('#form').submit(function (event) {
    event.preventDefault();

    $(this).find('.alert-danger').remove();

    var select_values = [];
    var filed_values = $("#form select").each(function (index, element) {

        select_values.push($(this).val());
    });

    // Count how many times an Header is selected in a form

    function check_double_headers(arr) {
        counts = {};
        val = true;

        $.each(arr, function (key, value) {
            console.log(key);
            console.log(value);
            if (!counts.hasOwnProperty(value) && value!=='-----') {
                counts[value] = 1;
            } else {
                counts[value]++;
            }
            return counts;
        });
        //console.log(counts)
         var dop = [];

        /*If header is selected twice or more push it into the array, after
          finds the element in array and appends an html error message to it
         */

        $.each(counts, function (key, value) {
            if (value >= 2) {
                dop.push(key);

                $.each(dop, function (index, element) {
                    //console.log(index);
                    // console.log(element);
                    error_form = $("#form select").filter(function () {

                        return this.value == element;
                    });
                    error_form.before('<div class="alert alert-danger alert-dismissible">' +
                        '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                        '<strong>Attenzione!</strong> Gli Headers non possono essere uguali</div>');

                    val = false;

                });
            }
        });
        return val
    }

    function check_required_fields(arr) {
        if ($.inArray("email", arr) !== -1) {

            return true;

        } else {
            alert("Email richiesta");
            return false;

        }
    }

    var headers = (check_double_headers(select_values));

    var required_fields = check_required_fields(select_values);

    //console.log(headers, required_fields)

    if (headers === true && required_fields === true) {

        $(this).unbind('submit').submit();
    }

});
