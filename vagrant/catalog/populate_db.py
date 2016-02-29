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
from catalog import db
from catalog.models import User, Category, Item

# TODO Create DB

# Add User
user = User(name="Robo Barista", email="tinnyTim@udacity.com",
            password="rabobarista", picture="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")  # noqa
db.session.add(user)
db.commit()

# Add Categories
categories = ['Soccer', 'Basketball', 'Baseball', 'Frisbee', 'Snowboarding',
              'Rock Climbing', 'Foosball', 'Skating', 'Hockey']
for category in categories:
    new_category = Category(name=category, user_id=1)
    db.session.add(new_category)
    db.commit()

# Soccer Items
category = Category.query.filter_by(name='Soccer').first()

name = "Two Shin Guards"
description = "A shin guard or shin pad is a piece of equipment worn on the front of a player’s shin to protect them from injury. These are commonly used in sports including association football (soccer), baseball, ice hockey, field hockey, lacrosse, rugby, cricket, and other sports. This is due to either being required by the rules/laws of the sport or worn voluntarily by the participants for protective measures."  # noqa
picture = "https://s-media-cache-ak0.pinimg.com/564x/dd/dc/39/dddc396a4585532a78b6d7caeea9f5b5.jpg"  # noqa

new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

name = "Shin Guards"
description = "Whether you're just starting out and are looking for a great price, or are a soccer star in the making and are looking for the highest quality, World Soccer Shop can keep your wallet and your shins out of pain with our great selection of shinguards."  # noqa
picture = "http://assets.academy.com/mgen/00/10269800.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

name = "Jersey"
description = "Soccer jerseys are an important piece of uniform for any soccer game. While a quick recreational game can be played in any athletic clothes, any soccer player can tell you that a good soccer jersey is necessary if you want to be comfortable and play at your best."
picture = "http://ilb.worldsportshops.com/Images/watermarked_thumbnail.aspx?photoNum=1&t=I&catalog=Soccer&img=28497.SW"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

name = "Soccer Cleats"
description = "Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. This does not happen in British English; the term 'studs' is never used to refer to the shoes, which would instead be known as 'football boots', 'rugby boots', and so on."
picture = "http://vignette3.wikia.nocookie.net/football/images/b/b4/Nike-HYPERVENOM-Phatal-Mens-Firm-Ground-Soccer-Cleat-599075_008_A.jpg/revision/latest?cb=20140204044848&path-prefix=en"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

# Snowboarding items
category = Category.query.filter_by(name='Snowboarding').first()
name = "Goggles"
description = "Protect the eyes from glare and from icy particles flying up from the ground. Double lens anti-fog ski goggles were invented and patented by Robert Earl \"Bob\" Smith."
picture = "http://www.snowlife.com.au/wp-content/uploads/2010/02/snowboarding-goggles.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

name = "Snowboard"
description = "Snowboards are boards that are usually the width of one's foot longways, with the ability to glide on snow. Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders. Commercial snowboards generally require extra equipment such as bindings and special boots which help secure both feet of a snowboarder, who generally rides in an upright position. These types of boards are commonly used by people at ski hills or resorts for leisure, entertainment, and competitive purposes in the activity called snowboarding."
picture = "http://skicarriage.co.uk/UserFiles/Image/White-Snowboard-With-Bindings.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()

# Frisbee items
category = Category.query.filter_by(name='Frisbee').first()
name = "Frisbee"
description = "A flying disc is a disc-shaped gliding toy or sporting item that is generally plastic and roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,[1] used recreationally and competitively for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in cross-section, allows it to fly by generating lift as it moves through the air while spinning. The term Frisbee, often used to generically describe all flying discs, is a registered trademark of the Wham-O toy company. Though such use is not encouraged by the company, the common use of the name as a generic term has put the trademark in jeopardy; accordingly, many \"Frisbee\" games are now known as \"disc\" games, like Ultimate or disc golf."
picture = "http://g01.a.alicdn.com/kf/HTB1bjepJpXXXXazXFXXq6xXFXXXT/1-piece-Professional-font-b-175g-b-font-27cm-Ultimate-Frisbee-Flying-Disc-flying-saucer-outdoor.jpg"
new_item = Item(name=name, description=description, category=category,
                picture=picture, user_id=1)
db.session.add(new_item)
db.commit()
