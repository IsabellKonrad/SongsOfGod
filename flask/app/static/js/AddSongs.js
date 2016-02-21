save_song = function(){
    var mode=0;
    if ($("#btn_mode_1").hasClass('active')){
        var mode = $("#btn_mode_1").val();
    }
    else if ($("#btn_mode_2").hasClass('active')){
        var mode = $("#btn_mode_2").val();
    }
    else {
        alert("No mode chosen")
    }
    var songtitle = $("#textarea_songtitle").val();
    if (mode != 0){
       var data = {"mode": mode, "songtitle": songtitle};
       $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: 'savesong',
          data: JSON.stringify(data),
          success: function(d){
            console.log(d.success)
          },
          error: function(obj, st, err){
          alert(err);
          }
       });
    }
}


check_new_song = function(){
  $("#btn_save_song").addClass("hidden");
  $("#btn_mode_2").remove();
  $("#btn_mode_1").remove();
  $("#select_mode").remove();
  $("#show_pdf_check").remove();
  var songtitle = $("#textarea_songtitle").val();
  var songcontent = $("#textarea_songcontent").val();
  var data = {"songtitle": songtitle, "songcontent": songcontent};
  var select_mode = $('<select />').css("width", "10%").prop("type","radio").addClass("btn btn_mode_suggestion")
    .attr("id","select_mode").on("change", function() {set_selected_mode(this);});
  var option = $('<option />').val("").text("andere Tonart");
  option.disabled = true;
  select_mode.append(option)
  var modes_vec = ["As","f","Es","c","B","g","F","d","C","a","G","e","D","h","A","fis","E","cis"];
  modes_vec.forEach(function(element){
    var option = $('<option />').text(element).val(element);
    select_mode.append(option);});
  $(select_mode).select2({
    minimumResultsForSearch: Infinity});

  $.ajax({
    contentType: 'application/json',
    type: 'POST',
    url: 'checksong',
    data: JSON.stringify(data),
    success: function(d){
      $("#show_pdf_check_placeholder").append(d.path);
      var mode1 = d.mode1;
      var mode2 = d.mode2;
      var btn_mode_1 = $('<button />').prop("type","radio").attr("id","btn_mode_1").text(mode1)
        .addClass("btn btn_mode_suggestion").css("margin-top", "-8%").css("margin-left","1%")
        .val(mode1).on("click", function() {set_selected_mode(this);});
      var btn_mode_2 = $('<button />').prop("type","radio").attr("id","btn_mode_2").text(mode2)
        .addClass("btn btn_mode_suggestion").css("margin-top", "-8%").css("margin-right","1%")
        .val(mode2).css("margin-left","1%").on("click", function() {set_selected_mode(this);});
      
      $("#btn_modes_placeholder").append(btn_mode_1);
      $("#btn_modes_placeholder").append(btn_mode_2);
      $("#btn_modes_placeholder").append(select_mode);
      $("#btn_modes_placeholder").removeClass("hidden");
    },
    error: function(obj, st, err){
      alert(err);
    }
  });
}


set_selected_mode = function(e) {
  $("#btn_save_song").removeClass("hidden");
  if (!$(e).hasClass('active')){
    $(e).addClass('active');
    $(e).siblings().removeClass('active');
    $(e).siblings().prop('selectedIndex', 0);
  }
}

$( document ).ready(function() {
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});