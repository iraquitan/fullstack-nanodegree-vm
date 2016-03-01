# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: populate_db
 * Date: 2/29/16
 * Time: 17:47
 * To change this template use File | Settings | File Templates.
"""
import os

from catalog import db
from catalog.models import User, Category, Item

# Create database if not exist
if not os.path.exists("./catalog/catalog.db"):
    db.create_all()

# Add User
user = User(name="Robo Barista", email="tinnyTim@udacity.com",
            password="robobarista", picture="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")  # noqa
db.session.add(user)
db.session.commit()

# Add Categories
categories = ['Soccer', 'Basketball', 'Baseball', 'Frisbee', 'Snowboarding',
              'Rock Climbing', 'Foosball', 'Skating', 'Hockey']
for category in categories:
    new_category = Category(name=category, user_id=1)
    db.session.add(new_category)
    db.session.commit()

# Soccer Items
category = Category.query.filter_by(name='Soccer').first()

name = "Two Shin Guards"
description = "A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury. These are commonly used in sports including association football (soccer), baseball, ice hockey, field hockey, lacrosse, rugby, cricket, and other sports. This is due to either being required by the rules/laws of the sport or worn voluntarily by the participants for protective measures."  # noqa
picture = "https://s-media-cache-ak0.pinimg.com/564x/dd/dc/39/dddc396a4585532a78b6d7caeea9f5b5.jpg"  # noqa
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Shin Guards"
description = "Whether you're just starting out and are looking for a great price, or are a soccer star in the making and are looking for the highest quality, World Soccer Shop can keep your wallet and your shins out of pain with our great selection of shinguards."  # noqa
picture = "http://assets.academy.com/mgen/00/10269800.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Jersey"
description = "Soccer jerseys are an important piece of uniform for any soccer game. While a quick recreational game can be played in any athletic clothes, any soccer player can tell you that a good soccer jersey is necessary if you want to be comfortable and play at your best."
picture = "http://ilb.worldsportshops.com/Images/watermarked_thumbnail.aspx?photoNum=1&t=I&catalog=Soccer&img=28497.SW"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Soccer Cleats"
description = "Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. This does not happen in British English; the term 'studs' is never used to refer to the shoes, which would instead be known as 'football boots', 'rugby boots', and so on."
picture = "http://www.royalsocceracademy.com/images/history-of-soccer-cleats6.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Soccer Ball"
description = "A football, soccer ball, or association football ball is the ball used in the sport of association football. The name of the ball varies according to whether the sport is called \"football\", \"soccer\", or \"association football\". The balls spherical shape, as well as its size, weight, and material composition, are specified by Law 2 of the Laws of the Game maintained by the International Football Association Board. Additional, more stringent, standards are specified by FIFA and subordinate governing bodies for the balls used in the competitions they sanction."
picture = "http://c.fastcompany.net/multisite_files/fastcompany/imagecache/inline-large/inline/2013/12/3022879-inline-s-6-2013-fifa-world-cup-brasil-ball.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Soccer Socks"
description = "These leg markings consist of short white ankle socks with green stripes on the back hooves, and puffy \"wrist bands\" on the front."
picture = "http://www.soccergarage.com/images/T/5-56.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Soccer Shorts"
description = "Soccer shorts similar to soccer jerseys should be able to let air come in. On some soccer shorts they have your number on them. Soccer shorts always have your team color so the coaches and refs can identify which players are which."
picture = "http://www.yomister.com/image/large/iPZ8kLwDTalalGc9k=NHj=Vr75RB65R8TuVDjYhh/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/1/3/13-14_nike_manchester_united_home_short.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "F.C. Barcelona - Jersey"
description = "FC Barcelona, also known as Barca, has given its fans reason to cheer in recent years due to their great success in Spain's First Division and the UEFA Champions League. Shop for your FC Barcelona soccer gear including the Barcelona soccer jersey at World Soccer Shop in the USA."
picture = "http://football2014wc.com/wp-content/uploads/2014/05/FC-Barcelona-2013-14-Home-Kit.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Arsenal Football Club - Jersey"
description = "Arsenal F.C. is one of the most storied clubs in English football history. Buy all your Arsenal soccer gear including the Arsenal soccer jersey at World Soccer Shop in the USA."
picture = "http://www.prodirectsoccer.com/productimages/V3_1_Main/84149.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Real Madrid - Jersey"
description = "Legendary players like Beckham, Raul, Owen, Ronaldo, and Zidane, have made Real Madrid one of the world's most popular, and successful teams. Buy all your Real Madrid soccer gear including the Real Madrid soccer jersey at World Soccer Shop in the USA."
picture = "http://www.scaryfootball.com/wp-content/uploads/2013/05/real-madrid-new-jersey-2013-2014-fly-emirates-official.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "F.C. Bayern Munich - Jersey"
description = "The Reds are one of the giants of European soccer, and Germany's Bundesliga."
picture = "http://jogjaartfestival.com/wp-content/uploads/2015/09/27703-fc-bayern-munich-201415-mens-official-away-jersey-740.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

# Snowboarding items
category = Category.query.filter_by(name='Snowboarding').first()
name = "Goggles"
description = "Protect the eyes from glare and from icy particles flying up from the ground. Double lens anti-fog ski goggles were invented and patented by Robert Earl \"Bob\" Smith."
picture = "http://www.snowlife.com.au/wp-content/uploads/2010/02/snowboarding-goggles.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Snowboard"
description = "Snowboards are boards that are usually the width of one's foot longways, with the ability to glide on snow. Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders. Commercial snowboards generally require extra equipment such as bindings and special boots which help secure both feet of a snowboarder, who generally rides in an upright position. These types of boards are commonly used by people at ski hills or resorts for leisure, entertainment, and competitive purposes in the activity called snowboarding."
picture = "http://skicarriage.co.uk/UserFiles/Image/White-Snowboard-With-Bindings.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

# Frisbee items
category = Category.query.filter_by(name='Frisbee').first()
name = "Frisbee"
description = "A flying disc is a disc-shaped gliding toy or sporting item that is generally plastic and roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,[1] used recreationally and competitively for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in cross-section, allows it to fly by generating lift as it moves through the air while spinning. The term Frisbee, often used to generically describe all flying discs, is a registered trademark of the Wham-O toy company. Though such use is not encouraged by the company, the common use of the name as a generic term has put the trademark in jeopardy; accordingly, many \"Frisbee\" games are now known as \"disc\" games, like Ultimate or disc golf."
picture = "http://g01.a.alicdn.com/kf/HTB1bjepJpXXXXazXFXXq6xXFXXXT/1-piece-Professional-font-b-175g-b-font-27cm-Ultimate-Frisbee-Flying-Disc-flying-saucer-outdoor.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

# Frisbee items
category = Category.query.filter_by(name='Hockey').first()
name = "Ice Hockey Stick"
description = "An ice hockey stick is a piece of equipment used in ice hockey to shoot, pass, and carry the puck. Ice hockey sticks are approximately 150-200 cm long, composed of a long, slender shaft with a flat extension at one end called the blade. The blade is the part of the stick used to contact the puck, and is typically 25 to 40 cm long. Stick dimensions can vary widely, as they are usually built to suit a particular player's size and preference. The blade is positioned at roughly a 135 degree angle from the axis of the shaft, giving the stick a partly 'L-shaped' appearance. The shaft of the stick is fairly rigid, but it has some flexibility to benefit some shots."
picture = "http://thehockeylocker.co.uk/image/cache/data/reebok-4k-composite-ice-hockey-stick-a1427-500x500.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

name = "Ice Hockey Puck"
description = "A hockey puck is a disk made of vulcanized rubber that serves the same functions in various games as a ball does in ball games. The best-known use of pucks is in ice hockey, a major international sport."
picture = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Ice_hockey_puck_-_2.jpg/1280px-Ice_hockey_puck_-_2.jpg?1456786414782"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.session.commit()

print("Database populated")
