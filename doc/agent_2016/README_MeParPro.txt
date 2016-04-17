AGENTE CON MEMORIA LIMITATA

Per l'agente con memoria limitata si è deciso di salvare le ultime quattro posizioni visitate e le quattro posizioni possibili in cui possono spostarsi gli altri agenti.
Il movimento avviene in maniera casuale cercando di escludere le posizioni già visitate nelle ultime quattro mosse e le posizioni in cui potrebbero andare le altre entità, se si hanno tutte e quattro le posizioni limitrofe impossibili da visitare ci si muove in una posizione casuale, in modo tale da non arrestare l'agente appena è contornato da celle indisponibili.
L'arresto avviene dopo che l'agente trova 50 celle già pulite consecutivamente, si è scelto 50 perchè sulle piste medio-grandi garantisce risultati migliori rispetto ad altri valori.
Abbiamo notato che se ci sono più agenti sulla stessa cella che provano a fare Suck solamente quello con l'id minore succhia effettivamente mentre gli altri perdono 20 punti, per ovviare a ciò abbiamo deciso di controllare se sono presenti uno o più agenti nella stessa cella guardandone l'id, se il mio è minore faccio il suck mentre se non lo è vado avanti in modo da perdere 5 punti anzichè 20.

AGENTE CON MEMORIA ILLIMITATA

Per gli agenti con memoria illimitata abbiamo implementato una visita in profondità puntando sul controllare tutta la pista e pulire tutte le celle piuttosto che evitare di fare bump.
Troviamo chi sono gli agenti appartenenti al team in base al loro nome e ne salviamo l'id, a seconda di questo i due agenti sviluppano la visita in direzioni diverse, uno controlla in ordine est, ovest, nord e sud mentre l'altro controlla in ordine sud, nord, ovest ed est.
I due agenti si salvano tutte le celle visitate sia da essi che dal compagno e il cammino che hanno svolto, in modo tale da poter tornare indietro una volta arrivato ad una "foglia".
L'agente non passa mai nelle celle visitate dal compagno di team mentre in quelle già visitate da lui ci ripassa solo per tornare indietro.
Anche qui abbiamo implementato il controllo degli id nel caso in cui più agenti si trovano sulla stessa cella, se è minore fa suck altrimenti va avanti.
L'agente si ferma una volta tornato alla cella da cui era partito.

