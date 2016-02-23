make_song_selector = function(){
  var div = $('<div />').addClass("placeholder_selectgroup");

  var select_song = $('<select />').attr("id","select_song").addClass("class_selected_songs")
      .css("width", "35%");
  div.append(select_song);
  $(select_song).select2({
    placeholder: "Lied"
  });

  var span_space = $('<span />').css("margin-left","5px").css("margin-right","5px");
  div.append(span_space);

  songlist.forEach(function(element){
    var option = $('<option />').text(element[1]).val(element[0]);
    select_song.append(option);
  });

  var btn_get_lyrics = $('<button />').addClass("btn btn-info").text("Get lyrics")
    .css("margin-left","5px").on("click", function() {get_lyrics();});
  div.append(btn_get_lyrics);
  return div;
};


get_lyrics = function(){
    var selected_song = $("#select_song").find(":selected").val();
    var data = {"selected_song": selected_song};
    console.log(data)
    $.ajax({
      contentType: 'application/json',
      type: 'POST',
      url: 'getsongedit',
      data: JSON.stringify(data),
      success: function(d){
        $("#show_lyrics_placeholder").text(d.lyrics);
      },
      error: function(obj, st, err){
        alert(err);
      }
    });

}


$( document ).ready(function() {
    $("#all_selected_songs_placeholder").append(make_song_selector());  

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});