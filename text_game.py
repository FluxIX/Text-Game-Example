#! /usr/bin/env python3

from enum import Enum

class Commands( Enum ):
   Traverse = "go to"
   Restart = "restart"
   QuitGame = "quit"
   Backtrack = "backtrack"

def main( **kwargs ):
   debug = kwargs.get( "debug", False )

   # Answer option value:
   # Value 0: operation
   # Value 1: parameter

   # Operations:
   # "go to": traverse to level <parameter>
   # "restart": restart the game
   # "quit": quit the game
   # "backtrack": backtrack <parameter> levels

   beginning_level = 0
   level_options = { beginning_level: ( "question 0", { "go to 1": ( Commands.Traverse, 1 ), "go to 2": ( Commands.Traverse, 2 ), "restart": ( Commands.Restart, 0 ), "quit": ( Commands.QuitGame, 0 ), } ), 
                     1: ( "question 1", { "go to 2": ( Commands.Traverse, 2 ), "back 1": ( Commands.Backtrack, 1 ), "restart": ( Commands.Restart, 0 ), "quit": ( Commands.QuitGame, 0 ), } ), 
                     2: ( "question 2", { "back 1": ( Commands.Backtrack, 1 ), "restart": ( Commands.Restart, 0 ), "quit": ( Commands.QuitGame, 0 ), } ),
                   } # clearly more could go here.

   try:
      level_stack = []
      quit = False

      while not quit:
         if not level_stack:
            level_stack.append( beginning_level )

         current_level = level_stack[ -1 ]
         level_question, options = level_options[ current_level ]

         print( "Level {:d}:".format( current_level ) )
         answer = input( "{}: {}> ".format( level_question, ", ".join( sorted( options ) ) ) )

         answer = answer.strip() # Be forgiving of leading and trailing whitespace.
         if answer in options:
            command, parameter = options[ answer ]

            if command == Commands.Traverse:
               level_stack.append( parameter )
               action_message = "Traversing to level {:d}.".format( parameter )
            elif command == Commands.Backtrack:
               for i in range( parameter ):
                  if level_stack:
                     level_stack.pop()
                  else:
                     break

               action_message = "Back-tracking {:d} step(s).".format( parameter )
            elif command == Commands.Restart:
               level_stack = []
               action_message = "Restarting game."
            elif command == Commands.QuitGame:
               quit = True
               action_message = "Quitting game."
            else:
               raise Exception( "Unsupported command: {}".format( command ) )

            if debug:
               print( action_message )
         else:
            print( "Invalid response: please try again." )
   except Exception as e:
      result = 1
      print( "Error {}".format( str( e ) ) )
   else:
      result = 0

   return result

if __name__ == "__main__":
   import sys
   sys.exit( main() )
