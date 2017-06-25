    function FixTable(Tableclass, FixColumnNumber, width, height) {
      /// <summary>
      ///   锁定表头和列
      ///   <para> sorex.cnblogs.com </para>
      /// </summary>
      /// <param name="Tableclass" type="String">
      ///   要锁定的Table的ID
      /// </param>
      /// <param name="FixColumnNumber" type="Number">
      ///   要锁定列的个数
      /// </param>
      /// <param name="width" type="Number">
      ///   显示的宽度
      /// </param>
      /// <param name="height" type="Number">
      ///   显示的高度
      /// </param>
      if ($("#" + Tableclass + "_tableLayout").length != 0) {
        $("#" + Tableclass + "_tableLayout").before($("#" + Tableclass));
        $("#" + Tableclass + "_tableLayout").empty();
      }
      else {
        $("#" + Tableclass).after("<div class='" + Tableclass + "_tableLayout' style='overflow:hidden;height:" + height + "px; width:" + width + "px;'></div>");
      }
      $('<div class="' + Tableclass + '_tableFix"></div>'
      + '<div class="' + Tableclass + '_tableHead"></div>'
      + '<div class="' + Tableclass + '_tableColumn"></div>'
      + '<div class="' + Tableclass + '_tableData"></div>').appendTo("#" + Tableclass + "_tableLayout");
      var oldtable = $("#" + Tableclass);
      var tableFixClone = oldtable.clone(true);
      tableFixClone.attr("class", Tableclass + "_tableFixClone");
      $("#" + Tableclass + "_tableFix").append(tableFixClone);
      var tableHeadClone = oldtable.clone(true);
      tableHeadClone.attr("class", Tableclass + "_tableHeadClone");
      $("#" + Tableclass + "_tableHead").append(tableHeadClone);
      var tableColumnClone = oldtable.clone(true);
      tableColumnClone.attr("class", Tableclass + "_tableColumnClone");
      $("#" + Tableclass + "_tableColumn").append(tableColumnClone);
      $("#" + Tableclass + "_tableData").append(oldtable);
      $("#" + Tableclass + "_tableLayout table").each(function () {
        $(this).css("margin", "0");
      });
      var HeadHeight = $("#" + Tableclass + "_tableHead thead").height();
      HeadHeight += 2;
      $("#" + Tableclass + "_tableHead").css("height", HeadHeight);
      $("#" + Tableclass + "_tableFix").css("height", HeadHeight);
      var ColumnsWidth = 0;
      var ColumnsNumber = 0;
      $("#" + Tableclass + "_tableColumn tr:last td:lt(" + FixColumnNumber + ")").each(function () {
        ColumnsWidth += $(this).outerWidth(true);
        ColumnsNumber++;
      });
      ColumnsWidth += 2;
      if ($.browser.msie) {
        switch ($.browser.version) {
          case "7.0":
            if (ColumnsNumber >= 3) ColumnsWidth--;
            break;
          case "8.0":
            if (ColumnsNumber >= 2) ColumnsWidth--;
            break;
        }
      }
      $("#" + Tableclass + "_tableColumn").css("width", ColumnsWidth);
      $("#" + Tableclass + "_tableFix").css("width", ColumnsWidth);
      $("#" + Tableclass + "_tableData").scroll(function () {
        $("#" + Tableclass + "_tableHead").scrollLeft($("#" + Tableclass + "_tableData").scrollLeft());
        $("#" + Tableclass + "_tableColumn").scrollTop($("#" + Tableclass + "_tableData").scrollTop());
      });
      $("#" + Tableclass + "_tableFix").css({ "overflow": "hidden", "position": "relative", "z-index": "50", "background-color": "Silver" });
      $("#" + Tableclass + "_tableHead").css({ "overflow": "hidden", "width": width - 17, "position": "relative", "z-index": "45", "background-color": "Silver" });
      $("#" + Tableclass + "_tableColumn").css({ "overflow": "hidden", "height": height - 17, "position": "relative", "z-index": "40", "background-color": "Silver" });
      $("#" + Tableclass + "_tableData").css({ "overflow": "scroll", "width": width, "height": height, "position": "relative", "z-index": "35" });
      if ($("#" + Tableclass + "_tableHead").width() > $("#" + Tableclass + "_tableFix table").width()) {
        $("#" + Tableclass + "_tableHead").css("width", $("#" + Tableclass + "_tableFix table").width());
        $("#" + Tableclass + "_tableData").css("width", $("#" + Tableclass + "_tableFix table").width() + 17);
      }
      if ($("#" + Tableclass + "_tableColumn").height() > $("#" + Tableclass + "_tableColumn table").height()) {
        $("#" + Tableclass + "_tableColumn").css("height", $("#" + Tableclass + "_tableColumn table").height());
        $("#" + Tableclass + "_tableData").css("height", $("#" + Tableclass + "_tableColumn table").height() + 17);
      }
      $("#" + Tableclass + "_tableFix").offset($("#" + Tableclass + "_tableLayout").offset());
      $("#" + Tableclass + "_tableHead").offset($("#" + Tableclass + "_tableLayout").offset());
      $("#" + Tableclass + "_tableColumn").offset($("#" + Tableclass + "_tableLayout").offset());
      $("#" + Tableclass + "_tableData").offset($("#" + Tableclass + "_tableLayout").offset());
    }
$(document).ready(function () {
      FixTable("MyTable", 1, 600, 400);
    });