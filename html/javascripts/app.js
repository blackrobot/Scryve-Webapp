$(document).ready(function(){
    var api_url = "http://api.scryve.com/",
        search_url = api_url + "search/",
        company_url = api_url + "company/";

    var company_html = "";

    $("#search form").submit(function(){
        $.getJSON(search_url + $(this).find('input').val(), function(data){
            $.each(data.companies, function(company){
                company_html += '<li><a href="#">' + company.name + '</a></li>';
            });

            $("#results ul").append(company_html);
        });
    });
});
