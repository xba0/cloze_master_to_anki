1. get the collection id from your browser, like "203/c/1949"
  a. open browser console
  b. click "manage" button in the deck; 
  c. check network pane of the console;
  d. you will see some url like https://www.clozemaster.com/api/v1/lp/203/c/1948
2. modify and run download_sentences.py to download the sentence pairs
3. in anki app, create anki card template like cloze_master.anki.card
4. create a card in anki using the template, and export it as txt with notes
4. modify and run generate_anki_card_set.py to generate card set using the format of the exported one
5. load the generated card set to anki
6. modify and run download_audios.py and follow https://forums.ankiweb.net/t/converting-audio-web-links-to-audio-files/30226/2
to move the downloaded media sources into the anki media directory
  the command is like: cp english-chinese/audios/* /mnt/c/Users/bao/AppData/Roaming/Anki2/<account>/collection.media
