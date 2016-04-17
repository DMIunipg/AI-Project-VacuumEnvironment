GUIDA VACUUM CLEANER PROJECT

Il gruppo è composto da Andrea Tavernelli, Gianmarco Stinchi e Katarzyna Habrajska.
Abbiamo realizzato due agenti, secondo le specifiche indicate nela mail delle consegne
da rispettare. Utilizzando l'environment fornitoci a lezione, sono stati scritti due file
python che rappresentano i due agenti pulitori: Super_Luigi_Multi_Vac e Super_Mario_Multi_Vaf.

SUPER_MARIO_MULTI_VAF:
L'ambiente in cui il robot si trova non è conosciuto a priori. Per questo motivo si è utilizzata 
un hash table che ad ogni movimento del robot viene aggiornata con le nuove informazioni.

#########INFORMAZIONI##########
self.pos = posizione corrente del robot
self.context = celle visitate dal robot

Inoltre anche le informazioni degli altri robot aggiornano il contesto 
(dove c'è un robot c'è una cella già pulita);

Alla scoperta di ogni nuova cella, si associa un array di possibili mosse effettuabili sulla cella stessa 
più il suo tipo (poichè la cella potrebbe essere un muro). Ogni volta che il robot trova sporco, pulisce,
altrimenti esegue le altre azioni rimanenti nella lista delle azioni, eliminandola dall'array 
riferito alla cella in cui si trova. Se viene a trovarsi in una cella senza azioni prima di terminare il lavoro
analizza il contesto e cerca la cella più vicina con ancora azioni rimanenti (Manhattan_distance). Se trova una cella 
con azioni rimanenti, usando l'algoritmo di Dijkstra, calcola lo shortest path verso quello cella e vi si dirige.

##########OTTIMIZZAZIONE COSTO############
Dai test eseguiti la soluzione trovata permette di pulire l'intera area, ma non di vincere sicuramente la sfida.
Per questo motivo si è fatta una relazione fra costo di raggiungimento di una cella da pulire ed il guadagno
derivante dalla pulizia della stessa. Ogni qualvolta viene pulita una cella, l'attributo "cost" viene 
impostato con valore = 100 (che è il guadagno per il successo dell'azione 'Suck'). Ad ogni azione l'attributo "cost"
viene decrementato di 6 punti (valore leggermente superiore del reale costo di movimento), mentre quando si ha una
collisione con il muro, viene reincrementato di 3 punti, perchè si è notato che nelle mappe con molti muri
tende a fermarsi prematuramente; se "cost" si azzera, il robot non eseguirà più azioni.

SUPER_LUIGI_MULTI_VAC:
L'agente VAC si muove eseguendo mosse puramente casuali, controllando unicamente se l'azione precedentemente 
ha prodotto 'Bump' non rieseguendo l'ultima mossa fatta.
