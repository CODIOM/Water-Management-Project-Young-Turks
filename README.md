test.py modelin falan test edildiği yer datada sıkıntı olduğundan biraz kötü tahminde bulunuyor ama idare eder durumda bunu çalıştırmadan direkt api.py'ı şu kodla: (uvicorn Water3.backend.api:app --reload) çalışıtrabilirsin.
O çalıştıktan sonra html file'ını tarayıcıya sürükleyin direkt vscodedan frontend açılıyor onu ben bilmiyom gemini öyle yaptı bıraktım bende şimdilik.
Çok basit structure, ai_core ailerin takıldığı yer ML ve LLM orda LLM de ben localde llama3.2 çalıştırdım sizde yerel model yoksa direkt API ile chatgpt, gemini falanda bağlayabilirsiniz sizde yoktur burda kodda yazan model Onu değiştirin YOKSA ÇALIŞMAZ
Şuan Data sıkıntı ve değerler hep 0 geldiğinden model tam öğrenemiyor düzgün datayla onu toparlayabiliriz ben şuan emrenin attığı: https://open-meteo.com/ dan aldım datayı data_processor.py da var kodu onuda değiştirebilirsiniz 
ML olarak Random Forrest var 

