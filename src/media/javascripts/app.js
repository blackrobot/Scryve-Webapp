$(document).ready(function(){
    var api_url = "http://api.scryve.com/",
    // var api_url = "http://localhost:8000/",
    // var api_url = "/",
        search_url = api_url + "search/",
        company_url = api_url + "company/";

    var company_html = "";
    var alternatives_html = "";

    function get_companies(val){
        $.getJSON(search_url + val + '/', function(data){
            if( data == undefined ){
                return;
            }
            company_html = "";

            $.each(data.companies, function(count, company){
                company_html += '<li><a href="#">' + company.name + '</a></li>';
            });

            $("#results").append(company_html);
            $("#results").attr("selected", "True");
            $("#search").attr("selected", "False");
        });
    };

    $("#search a").click(function(e){
        $("#backButton").show();
        e.preventDefault();
        get_companies($("#search input").val());
    });

    $("#search form").submit(function(e){
        $("#backButton").show();
        e.preventDefault();
        get_companies($("#search input").val());
    });

    $("#results li a").live('click', function(e){
        e.preventDefault();
        $("#backButton").show();

        $.getJSON(company_url + $(this).html() + '/', function(data){
            if( data == undefined ){
                return;
            }
            alternatives_html = "";

            $.each(data.alternatives, function(count, company){
                alternatives_html += '<div class="row"><span>' + company.name + ': ' + company.total_weighted_rating + '</span></div>';
            });

            $("#company").append('<fieldset><div class="row"><span>' + data.company.name + ": " + data.company.total_weighted_rating + '</span></div></fieldset>');

            $("#company").append('<h2>Alternatives</h2><fieldset>' + alternatives_html + '</fieldset>');
            $("#company").attr("selected", "True");
            $("#results").attr("selected", "False");
        });
    });
});
