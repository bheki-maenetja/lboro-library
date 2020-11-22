# Standard Library Imports
import json
import re

from random import choice

my_string = """
Girl Of The South
Doctor Without Shame
Descendants Without Duty
Phantoms Of The Ocean
Companions And Traitors
Invaders And Heirs
Decay Of Hell
Revenge With Wings
Sounds In Nightmares
Guarding The Fires
Five Minutes in China
Forty Winks at the Pyramids​
Abernethy on the Constitution
A Carpenter’s Bench of Bishops
Toot’s Universal Letter-Writer
Orson’s Art of Etiquette​
Downeaster’s Complete Calculator
History of the Middling Ages
Jonah’s Account of the Whale
Captain Parry’s Virtues of Cold Tar
Kant’s Ancient Humbugs​
Bowwowdom. A Poem
The Quarrelly Review
The Gunpowder Magazine
Steele. By the Author of ‘Ion’
The Art of Cutting the Teeth
Matthew’s Nursery Songs
Paxton’s Bloomers
On the Use of Mercury by the Ancient Poets
Drowsy’s Recollections of Nothing​
Heavyside’s Conversations with Nobody
Commonplace Book of the Oldest Inhabitant
Growler’s Gruffiology, with Appendix
The Books of Moses and Sons
Burke (of Edinburgh) on the Sublime and Beautiful​
Teazer’s Commentaries
King Henry the Eighth’s Evidences of Christianity
Miss Biffin on Deportment
Morrison’s Pills Progress
Lady Godiva on the Horse​
Munchausen’s Modern Miracles
Richardson’s Show of Dramatic Literature
Hansard’s Guide to Refreshing Sleep (as many volumes as possible)
History of a Short Chancery Suit
Catalogue of Statues of the Duke of Wellington
Lord Of The Solstice
Angel Of Eternity
Descendants Of The Void
Guardians With Money
Trees And Slaves
Humans And Giants
Means With Strength
Family Without Hope
Altering The Light
Visiting The Angels
Medic With Silver
Snake Of The Curse
Rebels Of Fortune
Fish Of The Plague
Mice And Women
Strangers And Cats
Demise Of History
Death Of Next Year
Dancing In My Friends
Weep For My Friends
Slave Without Hate
Heir Of Yesterday
Criminals With Silver
Dogs Of The Nation
Gangsters And Traitors
Criminals And Turtles
Scourge Of Heaven
Disruption Without Honor
Bathing In The End
Signs In A Storm
Companion Of The Nation
Lord Of Greatness
Horses Without Desire
Armies Of Reality
Hunters And Witches
Wolves And Spies
Shield Of Tomorrow
Dishonor Of Next Year
Inventing My Enemies
Meeting In The End
Parrot Of Fire
Vulture Of The Eternal
Blacksmiths Without Duty
Criminals Of Sorrow
Hunters And Phantoms
Owls And Foes
Extinction Of The Eternal
Ruins Of The Prison
Confessions Of The Town
Question My Husband
Vulture Of Dread
Witch Without Direction
Rebels Of The Sea
Invaders Of The End
Guardians And Slaves
Lions And Wolves
Root Of Rainbows
Tower With A Goal
Justice In The Animals
Painting Myself
Man Of The Stars
Medic Of Our Ship
Officers Of Earth
Martians Of Death
Armies And Mercenaries
Pilots And Heroes
Symbols Of The Droids
Honor Of Death
Intelligence In Droids
Gift Of A Rise Of Machines
Director On My Ship
Creator Of The Universe
Intruders Of Mars
Men With Tentacles
Creatures And Girls
Guardians And Defenders
Nation Of The Crash
Battle Of The Void
Secrets Of The Machines
Closed For Androids
Monster Who Smiles
Agent At The Convention
Cooks Looking At Me
Teachers In The Basement
Friends And Animals
Witches And Owls
Blood At The Convention
Music Next Door
Sweating In The Dungeons
Evil In The North
Witch In The Antique Shop
Vulture Who Stare
Fiends Of Detention
Humans In The Attic
Fish And Strangers
Demons And Vultures
Don't Look At The Hospital
Shadows At The Convention
Alive In The Fog
Surviving The Dungeons
Freak Of The Night
Bat With Fire
Freaks With A Smile
Imps Asks Weird Questions
Ghosts And Guests
Fish And Bats
Screams In The Lake
Noises On My Roof
Defenseless In Eternity
Weeping At The Elements
Cook At The River
Monster Without Teeth
Trees In My Garden
Dogs Without Teeth
Women And Humans
Fiends And Demons
Rituals Hiding From Me
Ambushed In The Field
Pained By The Swamp
Haunted In The Mountains
Angel Who Stare
Fiend During Full Moon
Cooks In The Forest
Phantoms With Black Hair
Students And Teachers
Vultures And Visitors
Giggling At The Convention
Bodies In The Fog
Living In Nightmares
Defenseless In Time
Doctor In The Fog
Imp In The Mist
Men In The Lake
Boys In The Forest
Guests And Girls
Crows And Wolves
Lost At The Graveyard
Paintings In The Antique Shop
Defiant In My Demise
Abandoned In The Graves
Horse Delusion
Harlequin Abroad
Rat Has Been Naughty
Lord Of Humor
Serpent And Wife
Fool And Wife
Traps Job
Whispers From The Forests
Word Of That Idiot
Shame Of Magic
Court Of The Dagger
Heir With A Goal
Druids Of The East
Necromancers Of Snow
Fighters And Lords
Curse Of The Eclipse
Hydra Of The Gods
Snakes Of Ice
Priests With Immortality
Creators And Vultures
Spiders And Officers
Revival Of Twilight
Birth Of The Night
Dwelling In The Future
Shelter In Shields
Troll Of Glory
Army Of The Banished
Robots Of Earth
Ghosts Of The North
Butchers And Horses
Serpents And Heroes
Destiny Of Wind
Crossbow Of Time
Meeting At My Friends
Learning From The Angels
Girl Without A Home
Enemy Of The Sword
Druids With Silver
Sages Of The End
Fish And Humans
Warlocks And Demons
Goal Without Sin
Culling Of The Mountain
Possessed By The Home Of Demons
Healing My Destiny
Baby Of Fantasy
Fox In The Forest
Tigers Of Wonder
Lions Of Stone
Ghosts And Rabbits
Boys And Dragons
Statue Of Mystery
Town In My Town
Gift Of My Cat
Amazing World Of My New Dog
Little Duck Of Fire
Little Boy In My School
Bears Of My Land
Cats Of Sunshine
Kittens And Ghosts
Goats And Cows
Coat In My Town
Statue Of Fantasy
Cleaning With My Pet Dragon
Foolish With My Dog
Chicken Of Rainbows
Family In My Town
Bears Of Dreams
Little Birds Of The Moon
Bunnies And Bunnies
Tigers And Bears
Pocket Of Silver
Week Of Secrets
Free With My Imagination
Giving With The School
Ghost In The Forest
Puppy Of Riddles
Mice Of Puzzles
Ghosts In The Forest
Boys And Foxes
Lions And Owls
Pocket Of The Sun
Lantern In Space
Back To Flowers
Caring For My Pet
Assistant With Debt
Dog Of Dusk
Butchers Without Duty
Bringers Of Last Rites
Pirates And Widows
Planners And Scientists
Demise Of The West
Ascension Of The Frontline
Searching At The Curse
Battle The King
Foreigner Of The Stockades
Lord Without A Head
Wolves Of Suffering
Warriors Of The Prison
Children And Witches
Agents And Horses
End Of Darkness
Border Without A Goal
Death To The Guards
Welcome To The Prisoners
Bearer Of The Curse
Friend Of Time
Vultures Without Direction
Girls Of Last Rites
Scientists And Blacksmiths
Horses And Bringers
Union Of History
Chase Of The Stars
Prepare For The Mountains
Adopting The Elements
"""
string_list = [i for i in my_string.strip().split('\n')]
print(len(string_list))
# Loading files
json_file = open("data.json", "r")
text_file = open("database.txt", "a")
data = json.load(json_file)

print(type(data), type(data[0]['category']))
input("Wait >> ")
for book in data:
    book['member_id'] = None
    book['isbn'] = book['isbn'].replace('-', '').replace('X', '0')
    book['title'] = string_list[data.index(book)]
    book['category'].append(choice(['sci-fi', 'fantasy', 'drama', 'horror', 'adventure']))
    text_file.write(json.dumps(book) + "\n")

text_file.close()
json_file.close()
input("Load data into database >>> ")
database = open("database.txt", "r")
for book in database:
    new_data = json.loads(book)
    print(new_data['id'], new_data['isbn'], new_data['title'], new_data['author'])

# database.close()

