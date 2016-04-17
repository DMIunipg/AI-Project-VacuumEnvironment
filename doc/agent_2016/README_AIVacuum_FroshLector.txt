             _____________________________
            |                             |
            |       ExeedAgentFrosh       |
            |_____________________________|

                                                 
                        .-::-.  `````             
                       :/o/Ndo/hhyshNMNd+-:/o+/:` 
   `.`                ./sMNMMN//odms/soyhssN+mNo/.
`://///:-`            `//ymmdo////////////hMMMMy/:
./////////:`           /s//////////////////syyo+/`
   .```.:///.         :y+////oyhddmmmdhs+//////N/ 
         -///.        +s//sys+/+syyyyyyyhhs////ss 
          :///       :s/shy..sy+ +yyy:`--`+ho//oh 
           ///-      :/hMy+ sMMM.:yy/ mMMy +yy/+m 
           -///      :+MMys. /+-`oyy/ sNd: +hMs/+ 
           `+/+      .+mMsoss++oyysyy+-..:oyNMh/. 
            ///.      .:hdyyyyyyssssyyyyysohMm+-  
            ///.      ```-/oyyysssssssyyyyhds:.   
            -//-            `+hyssyyyho/:-.` `    
            `+//           -/+.-/++/-/+-          
             -///`        :/+:       -+/-         
              -///-`     ://+-       :+//.        
               `:///:-..:///+/      ./:+//        
                 `-:////+++o///.` `-//-:++        
                     ``...`:////-:////`           
                           -///.  -//+            
                          `///+   .///-           
                          `::-`    -::-           
                                            

This agent can remember:
    - the direction from where it comes
    - the last bump it has done
    - the number of bumps for any direction
    - the number of clean tiles for any direction
    - the number of consecutive clean tiles
    - the last position of the other agents

The agent decides the next move using an evaluating function that takes account of all the percepts. The number of bumps and clean tiles are used to decrease the posibility to go in the direction where one can find more and the relative position of the other agents prevents to cross and visit already clean areas. The last bump position is the only non additive variable: indeed it is a factor which is zero if the direction considered is the last bump direction, so the possibilities to go there become 0. The evaluating function use a random seed to encrease the posibilities to get into narrow areas of the map.
The agent stops itself after 50 consecutive clean tiles.


 *----------**----------**----------**----------**----------*
 
 
 
 
             ______________________________
            |                              |
            |       ExeedAgentLector       |
            |______________________________|



      ys/`              `/oy.                     
     :sodds:          :sddso:                     
     o+/sdddy:`....`/hdddy///                     
     sooyddddddddddddddddy/o:                     
     ohohddddddddddddddddhod`                     
     :dhdddddddddddddddddddo                ```   
      hdh+/::/+yhhy+/::+sddy            -/os:--:- 
     -dh::------::-------+dd`        .+hdddh+:::` 
     /do-:::---:-:---:::--hd:      .sdddds/.`     
    `hdy:`.yo-:/-/:-/h.`.:dd/     :hddh+`         
   /hddd+:-...--:---...--yddh:`  :ddds`           
 ``+dh+/-------:o:------:/+dddo .ddds             
  ``-//::---:::::::::----:+hs-``+ddh`             
    :/oo:+:------------::--  `  yddo              
    -:oyydddhso++++syyy-        hdd+              
       -yddyydhsssdhyhdds.     `ddd-              
         -hyyy+---yyyhhddh`    sddy               
         +yyyh:---yyyyddd:   .sddh.               
         yyyhs----oyyyys` .:sdddy.                
         .hhho----/yhhmdddddddy:                  
          hddhso+oshddmddhs+:`                    
          ydddy/-:sdddy                           
          sddd`    oddd.                          
        `:/osy     -soo/:                         
        .:/---      -:::-     


This Agent can remember (in addition to all the previous things):
    - the direction from which it comes
    - the position of all the walls found
    - the position of all the tiles visited by itself or by other agents (friend or foe)
        
The ability to remember the configuration of the whole map allows to determine with more precision the direction in which it is better to go. The agent will prefer not yet explored areas and it will avoid going in the direction of clean tiles, walls or other agents. Moreover, the evaluating function used to choose the next move uses the walls' absolute positions in order to estimate the size of the map and thus the number of tiles. This, combined with the knowledge of the visited tiles allows the agent to stop when the number of clean tiles is near to the estimated size.


*----------**----------**----------**----------**----------*