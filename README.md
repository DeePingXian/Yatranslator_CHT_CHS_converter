# Yatranslator繁簡中文本轉換工具

## 簡介
本項目基於OpenCC開放中文轉換<br>
由於幾乎所有COM3D2的民間中譯文本都是簡體的，所以做了這程式出來，方便轉成繁體<br>
此程式可以把Yatranslator翻譯文本每行的後段（即譯文），進行繁簡互轉，且OpenCC支援大陸台灣及日常慣用語轉換，所以也一並做了進去<br>
Yatranslator翻譯文本的格式：TAB分隔日中文本、換行區隔翻譯項目<br><br>

## 使用說明
放置此程式的資料夾路徑請盡量只包含英數，以降低出錯機率<br>
使用時將要轉換的文本置於與「converter.exe」同一目錄的「before」資料夾下（沒有就創建一個），可包含資料夾，但不支援zip檔，請先解壓縮<br>
轉換完的文本會自動置於「after」資料夾下，若該資料夾已存在，則會存於往後編號的的資料夾<br>
轉換錯誤的那行文本會直接照抄並提示，不進行轉換；若檔案不是txt檔的話會跳過並提示<br>
當一檔案的文本在51行以上時會使用多核並行轉換，以加快轉換速度，50行以下則不使用，避免分配工作消耗太多時間<br>

***

## 實測效能
<table>
<tr><td align="center" colspan = "2">單核簡轉繁（包含慣用語）</td></tr>
<tr><td>CPU</td><td>效能</td></tr>
<tr><td>Intel® Core™ i5-9400F</td><td>約29.5行/s</td></tr>
<tr><td>AMD Ryzen™ 7 3700X PBO FCLK 1500MHz</td><td>約37行/s</td></tr>
<tr><td>AMD Ryzen™ 7 3700X @4.2GHz FCLK 1833MHz</td><td>約37行/s</td></tr>
<tr><td>AMD Ryzen™ 7 7700X PBO FCLK 2000MHz</td><td>約70行/s</td></tr>
</table><table>
<tr><td align="center" colspan = "2">多核簡轉繁（包含慣用語）</td></tr>
<tr><td>CPU</td><td>效能</td></tr>
<tr><td>Intel® Core™ i5-9400F</td><td>約122行/s</td></tr>
<tr><td>AMD Ryzen™ 7 3700X PBO FCLK 1500MHz</td><td>約300行/s</td></tr>
<tr><td>AMD Ryzen™ 7 3700X @4.2GHz FCLK 1833MHz</td><td>約330行/s</td></tr>
<tr><td>AMD Ryzen™ 7 7700X PBO FCLK 2000MHz</td><td>約450行/s</td></tr>
</table>

***

## 使用規範
此程式允許任何形式的使用、修改、打包、轉發，不需經本人同意，也可以加進自己的專案中。轉換它人的文本，除個人使用外之用途請經文本主人同意。
