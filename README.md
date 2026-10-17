Die zunehmende Digitalisierung im medizinischen Bereich führt zu einer wachsenden Menge digital vorliegender
medizinischer Dokumente. Arztbriefe enthalten eine Vielzahl relevanter Informationen, die für die weitere Behandlung
von Patientinnen und Patienten, für administrative Prozesse sowie für medizinische Forschungszwecke benötigt werden. 
Ein wesentlicher Teil dieser Informationen liegt jedoch weiterhin in unstrukturierter beziehungsweise semi-strukturierter 
Form vor. Insbesondere Patientendaten, Behandlungszeiträume und Diagnosen müssen häufig manuell aus Dokumenten erfasst, 
übertragen und für eine weitere Verarbeitung strukturiert aufbereitet werden.
Die manuelle Verarbeitung dieser Informationen ist mit einem erheblichen Zeitaufwand verbunden und birgt gleichzeitig das 
Risiko von Übertragungs- und Erfassungsfehlern. Dies betrifft insbesondere die Übertragung medizinischer Diagnosen und deren 
Zuordnung zu standardisierten ICD-Codes. 
Zusätzlich können bei der automatisierten Texterkennung durch OCR Fehler entstehen, beispielsweise durch falsch erkannte 
Zeichen oder die fehlerhafte Erkennung medizinischer Fachbegriffe. Dadurch besteht die Herausforderung nicht nur darin, 
Informationen aus einem medizinischen Dokument zu extrahieren, sondern diese anschließend auch inhaltlich korrekt zu 
interpretieren, zu normalisieren und strukturiert weiterzuverarbeiten.
Vor diesem Hintergrund bietet die Kombination aus Optical Character Recognition (OCR), Large Language Models (LLMs) und 
datenbankgestützten Verfahren die Möglichkeit, bisher manuell durchgeführte Verarbeitungsschritte zumindest teilweise zu 
automatisieren. Durch die automatisierte Erkennung und Strukturierung relevanter Informationen könnten medizinische Dokumente 
effizienter verarbeitet und die gewonnenen Daten für nachgelagerte Anwendungen nutzbar gemacht werden.
Im Rahmen dieser Arbeit wurde bereits ein prototypisches System auf Basis der Programmiersprache Python entwickelt. Das System
ermöglicht die Verarbeitung eines Bildes beziehungsweise Screenshots der ersten Seite eines Arztbriefes. 
Über eine OCR-Komponente werden die im Dokument enthaltenen Informationen erkannt und anschließend mithilfe eines Large 
Language Models strukturiert verarbeitet. Dabei werden unter anderem der Name der Patientin beziehungsweise des Patienten, 
das Geburtsdatum, der Behandlungszeitraum sowie vorhandene Diagnosen extrahiert. Erkannte Diagnosen werden anschließend 
mithilfe einer eingebundenen Datenbank mit hinterlegten Diagnosen, ICD-Codes und möglichen OCR-verfälschten Diagnosefragmenten
abgeglichen. Auf diese Weise sollen auch fehlerhaft erkannte oder fragmentierte medizinische Begriffe einer korrekten Diagnose
und einem entsprechenden ICD-Code zugeordnet werden können.
Die Ergebnisse werden anschließend strukturiert in einer Excel-Datei ausgegeben. Dabei werden sowohl die durch OCR 
beziehungsweise das System erkannten Informationen als auch die daraus abgeleiteten beziehungsweise korrigierten Diagnosen und
die zugehörigen ICD-Codes dargestellt. Zusätzlich wird ein Konfidenzwert beziehungsweise eine Einschätzung der 
Erkennungssicherheit ausgegeben, um eine nachträgliche Überprüfung auffälliger Ergebnisse zu ermöglichen.
Das entwickelte System stellt damit einen ersten prototypischen Ansatz zur automatisierten Verarbeitung medizinischer 
Dokumente dar. Der aktuelle Funktionsumfang konzentriert sich zunächst auf wesentliche Informationen der ersten Seite eines 
Arztbriefes. Eine zukünftige Erweiterung könnte die Verarbeitung vollständiger Arztbriefe sowie die Extraktion weiterer 
medizinischer Informationen umfassen. 
Darüber hinaus besteht die Möglichkeit, die strukturiert aufbereiteten Daten nicht nur in Excel auszugeben, sondern direkt in 
Datenbanksysteme beziehungsweise Forschungsdatenbanken zu überführen.
