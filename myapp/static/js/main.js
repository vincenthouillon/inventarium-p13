/*!
 * Bootstrap Auto-dismiss alerts
 * Mario Juárez <mario@mjp.one>
 * https://github.com/mariomka/bootstrap-auto-dismiss-alert
 * Licensed under the MIT license
 */

;(function ($) {

    'use strict';

    $('.alert[data-auto-dismiss]').each(function (index, element) {
        var $element = $(element),
            timeout  = $element.data('auto-dismiss') || 3000;

        setTimeout(function () {
            $element.alert('close');
        }, timeout);
    });

})(jQuery);


/*!
* To make an entire row in a hotspot as a link
*/

jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});