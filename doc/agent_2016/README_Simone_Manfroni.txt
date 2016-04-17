L'agente Manfro e' un agente random, ovvero un Multi Vacuumcleaner Agent with Constant memory.
Compie 4 azioni di spostamento:
-GoEast; 
-GoWest;
-GoNorth;
-GoSouth.
Ogni volta che si trova in uno stato Dirty, compie un'azione di Suck.
L'unico accorgimento che porta seco e' quello di evitare di compiere nuovamente la mossa che lo ha portato ad un Dump.



L'agente Manfro2 e' invece un agente con memoria, ossia un Multi Vacuumcleaner Agent with Free memory. Esso eredita gran parte dell'agente Manfro ed inoltre ha:
-una funzione "update" che aggiorna la posizione, indicizzata con (0, 0) all-inizio, in base all'ultima azione;
-dichiarazione di ultima azione inizialmente vuota. Se non risulta in memoria, aggiungo tutte le azioni; a quel punto se è dirty e c'è suck nella lista, faccio suck ed estraggo suck dalla lista,poi il resto è simile al random, solo che prima cerca di finire le azioni e se non ce ne sono si muove a caso.
-un contatore che ferma l-agente se gli spazi che ha pulito sono maggiori di 25




















N.B.: l'agente Manfro ha spesso battuto l'agente Manfro2 in una simulazione di prove ripetute. 
