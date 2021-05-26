  
  

**endpoint**: `/fanfic/<int:index>`

  

allowed method: `GET`

  

description: Given the index of a fanfic, this call returns the top 50 fanfics similar to this fanfic, along with their metadata (or just the meta data of the fanfic depending on the parameter). Use this for fanfiction display page only. The index used should be returned from this API, not an arbitrary value provided by the user or any other source

  

parameters:

  

`return_sim` (*bool*): `[1|0]`

- description: `1` for returning similar fanfics, `0` for not returning. (not returning is ~200x faster than returning)


response:

```

{

	'main': {
		'some metadata'
	}, # metadata of the fanfic you asked for

	'similar`: {

		1: 'some metadata',

		2: 'some metadata',

		....

		50: 'some metadata'

	} # ranked similar fanfics; will be empty if return_sim == 0

}

```

example
`.../fanfic/1234?return_sim=1`
`.../fanfic/32?return_sim=0`



error:

- 404 if index is out of range (this shouldn't happen because you always get the index from the API in the first place)

  

**endpoint**: `/query`

  

allowed method: `GET`

  

description: This endpoint handles the user query and return the fanfics according to the query. Query can have three types:

  

1. a chunk of freeform text, this could even be another fanfic.

  

2. a fandom -- this is for the case the user just wants to explore a certain fandom.

  

3. a combination of characters/cp/tags.

  

*notice: this implies that it can only be ONE of the three types*

  

form data:

  

`user_input` (*str*):

- (1) description: whatever the user wants to input. any text. (there's a file called `sample.txt` which you can use to test)

  

`fandom` (*str*):

- (2) description: a fandom name (only support one right now). user will select from auto-complete. They can not freeform edit this. Right now the algorithm returns fanfics sorted by their kudos if that fandom has more than 50 fanfics in the database, otherwise it prioritizes fanfics from fandoms that are closest to the target fandom

  

`characters` (*str*):

- (3) description: a list of character names, seperated by comma. we provide auto-complete, but this could be any character name they want.

  

`relationships` (*str*):

- (3) description: a list of cps, each cp is seperated by a comma, the two characters of that cp is seperated by "/". this cp could be anything, and any character name

  

`tags` (*str*):

- (3) description: any tags they want, seperated by a comma

  
  

response:

```

{

	1: 'some metadata',

	2: 'some metadata',

	...

	50: 'some metadata'

} # ranked similar fanfics according to user's query

```

  

example request:

  

EX 1

```

user_input:'this could literally be a copy/paste of another fanfic'

fandom:''

characters:''

relationships:''

tags:''

```

  

EX 2

```

user_input:''

fandom: 'Minecraft'

characters:''

relationships:''

tags:''

```

  

EX 3

```

user_input:''

fandom: ''

characters:'george,dream,tommy'

relationships:'george/dream,tommy/wilbur,xyz/abc'

tags:'romance,prince and princess,lol,wait no,this could a really long sentence'

```

EX 4
```

user_input:''

fandom: ''

characters:''

relationships:''

tags:'all mcyt youtubers are college roommates'

```

EX 5
```
user_input:''

fandom: ''

characters:''

relationships:'tony stark/peter park'

tags:''

```

  

error:

- 400 if all arguments are empty or if the given fandom does not exist in the database

  
  

**endpoint**: `/meta/<string:cat>`

  

allowed method: `GET`

  

description: give the frontend a list of characters/cps/tags/fandoms/other_metadata currently in the database to help with auto-complete and information display.