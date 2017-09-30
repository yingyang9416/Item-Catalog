from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Library, Base, Book, User

engine = create_engine('sqlite:///librarybookswithuser.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Steven Yang", email="yingyang9416@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Thompson Library
library1 = Library(user_id=1, name="Thompson Library")

session.add(library1)
session.commit()


book1 = Book(user_id=1, name="INTRODUCING POLITICAL PHILOSOPHY", description="Essential illustrated guide to key ideas of political thought. ",
                     published_year=2011, author="DAVE ROBINSON", library=library1)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="INTRODUCING MARX", description="Compact INTRODUCING guide to the influential philosopher, sociologist and economist.",
                     published_year=2012, author="RIUS", library=library1)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="INTRODUCING BARTHES", description="INTRODUCING guide to the cult author, semiologist and analyzer of advertising, Roland Barthes.",
                     published_year=2011, author=" Nidhi Agrawal", library=library1)

session.add(book3)
session.commit()

book3 = Book(user_id=1, name="A cute love story", description="""Aakriti is in love with Neeraj.Neeraj is also mad for Aakriti.but she found out him not to be a good boy.will she be able to change him?
will their love win over the weaknesses of Neeraj? will they have happy life together?""",
                     published_year=2010, author="PHILIP THODY", library=library1)

session.add(book3)
session.commit()

book3 = Book(user_id=1, name="New Life", description="""Mia Owens and her mother have just moved to California from England to find a better life.
Mia just wants to live easy, go to school, hag out with friends... that was until Ian Marsh turned her life upside down. """,
                     published_year=2013, author="H.N. S.", library=library1)

session.add(book3)
session.commit()

book3 = Book(user_id=1, name="Ultimate Pleasure", description="""	
A girl who hits the clubs every other day and sleeps with 1 diffrent guy every other day until she finds the perfect guy. Her own personal sex god.""",
                     published_year=2010, author=" Rachel G", library=library1)

session.add(book3)
session.commit()

# 18th Avenue Library
library2 = Library(user_id=1, name="18th Avenue Library")

session.add(library2)
session.commit()


book1 = Book(user_id=1, name="Heredity: A Very Short Introduction", description="Provides an overview of over two thousand years of human thought on the subject of heredity.",
                     published_year=2017, author="John Waller", library=library2)

session.add(book1)
session.commit()


book3 = Book(user_id=1, name="New Life", description="""Mia Owens and her mother have just moved to California from England to find a better life.
Mia just wants to live easy, go to school, hag out with friends... that was until Ian Marsh turned her life upside down. """,
                     published_year=2013, author="H.N. S.", library=library2)

session.add(book3)
session.commit()

book3 = Book(user_id=1, name="Ultimate Pleasure", description="""	
A girl who hits the clubs every other day and sleeps with 1 diffrent guy every other day until she finds the perfect guy. Her own personal sex god.""",
                     published_year=2010, author=" Rachel G", library=library2)

session.add(book3)
session.commit()

# Central Park Library
library3 = Library(user_id=1, name="Central Park Library")

session.add(library3)
session.commit()

book3 = Book(user_id=1, name="New Life", description="""Mia Owens and her mother have just moved to California from England to find a better life.
Mia just wants to live easy, go to school, hag out with friends... that was until Ian Marsh turned her life upside down. """,
                     published_year=2013, author="H.N. S.", library=library3)
session.add(book3)
session.commit()

book1 = Book(user_id=1, name="INTRODUCING POLITICAL PHILOSOPHY", description="Essential illustrated guide to key ideas of political thought. ",
                     published_year=2011, author="DAVE ROBINSON", library=library3)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="INTRODUCING MARX", description="Compact INTRODUCING guide to the influential philosopher, sociologist and economist.",
                     published_year=2012, author="RIUS", library=library3)
session.add(book2)
session.commit()

book3 = Book(user_id=1, name="INTRODUCING BARTHES", description="INTRODUCING guide to the cult author, semiologist and analyzer of advertising, Roland Barthes.",
                     published_year=2011, author=" Nidhi Agrawal", library=library3)
session.add(book3)
session.commit()

book1 = Book(user_id=1, name="Heredity: A Very Short Introduction", description="Provides an overview of over two thousand years of human thought on the subject of heredity.",
                     published_year=2017, author="John Waller", library=library3)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="Heredity: A Very Short Introduction", description="Provides an overview of over two thousand years of human thought on the subject of heredity.",
                     published_year=2017, author="John Waller", library=library3)

session.add(book2)
session.commit()

# Fine Arts Library
library4 = Library(user_id=1, name="Fine Arts Library")

session.add(library4)
session.commit()

book3 = Book(user_id=1, name="INTRODUCING BARTHES", description="INTRODUCING guide to the cult author, semiologist and analyzer of advertising, Roland Barthes.",
                     published_year=2011, author=" Nidhi Agrawal", library=library4)
session.add(book3)
session.commit()

book1 = Book(user_id=1, name="Heredity: A Very Short Introduction", description="Provides an overview of over two thousand years of human thought on the subject of heredity.",
                     published_year=2017, author="John Waller", library=library4)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="Heredity: A Very Short Introduction", description="Provides an overview of over two thousand years of human thought on the subject of heredity.",
                     published_year=2017, author="John Waller", library=library4)

session.add(book2)
session.commit()






print "added menu items!"
