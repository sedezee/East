import time 
import time_zone
import discord

def case(str_input, first_cap): 
    if isinstance(str_input, str) and isinstance(first_cap, bool):
        caseChange = ("Admin", "Dev", "Joke", "Command")
        str_input = str_input.lower()
        for item in caseChange: 
            if item.lower() in str_input: 
                str_input = str_input.replace(item.lower(), item)
        
        if not first_cap: 
            str_input = str_input[:1].lower() + str_input[1:]
        
        return(str_input)
    else: 
        print("Please input a string and a boolean.")

def snake_case(str_input, to_snake): 
    div = ("admin", "dev", "joke")
    str_input = str_input.lower() 

    if isinstance(str_input, str) and isinstance(to_snake, bool) and to_snake: 
        for item in div: 
            if item in str_input:
                str_input = str_input.replace(item, item + "_")
        return str_input
    elif isinstance(str_input, str) and isinstance(to_snake, bool) and not to_snake and '_' in str_input:
        return str_input.replace('_', '')

    else: 
        print("Please input a string and two booleans")

def to_bool(arg):
    try: 
        if isinstance(arg, str): 
            arg.lower()

        evalBool = {}
        evalBool.update(dict.fromkeys(['true', 'y', 't', 1], True))
        evalBool.update(dict.fromkeys(['false', 'n', 'f', 0], False))
        
        return evalBool[arg]
    except: 
        return(f"{arg} is not a boolean argument. Please input a boolean argument.")

def get_time(time_zone, military_time, return_time): 
    time_zones = {
        "ACDT" : [10, 30],
        "ACST" : [9, 30],
        "ACT" : [-5, 0],
        "ADT" : [-3, 0],
        "AEDT" : [11, 0],
        "AEST" : [10, 0],
        "AFT" : [4, 30], 
        "AKDT" : [-8, 0],
        "AKST" : [-9, 0],
        "ALMT" : [6, 0],
        "AMST" : [-3, 0],
        "AMT" : [-4, 0], 
        "AMT2" : [4, 0], 
        "ANAT" : [12, 0], 
        "AQTT" : [5, 0],
        "ART" : [-3, 0],
        "AST" : [-4, 0], 
        "AST2" : [3, 0],
        "AWST" : [8, 0],
        "AZOT" : [1, 0],
        "AZT" : [4, 0], 
        "BDT" : [8, 0],
        "BIOT" : [6, 0],
        "BIT" : [-12, 0],
        "BOT" : [-4, 0],
        "BRST" : [-2, 0],
        "BRT" : [-3, 0],
        "BST" : [1, 0], 
        "BST2" : [6, 0],
        "BST3" : [11, 0],
        "BTT" : [6, 0],
        "CAT" : [2, 0],
        "CCT" : [6, 30],
        "CDT" : [-5, 0],
        "CDT2" : [-4, 0],
        "CEST" : [2, 0],
        "CET" : [1, 0],
        "CHADT" : [13, 45],
        "CHAST" : [12, 45], 
        "CHOT" : [8, 0],
        "CHOST" : [9, 0],
        "CHST" : [10, 0],
        "CHUT" : [10, 0], 
        "CIST" : [-8, 0],
        "CIT" : [8, 0], 
        "CKT" : [-10, 0],
        "CLST" : [-3, 0], 
        "CLT" : [-4, 0], 
        "COST" : [-4, 0], 
        "COT" : [-5, 0], 
        "CST" : [-6, 0],
        "CST2" : [8, 0], 
        "CST3" : [-5, 0],
        "CT" : [8, 0],
        "CVT" : [-1, 0],
        "CWST" : [8, 45],
        "CXT" : [7, 0], 
        "DAVT" : [7, 0],
        "DDUT" : [10, 0],
        "DFT" : [1, 0],
        "EASST" : [5, 0],
        "EAST" : [-6, 0],
        "EAT" : [3, 0],
        "ECT" : [4, 0],
        "ECT2" : [-5, 0],
        "EDT" : [-4, 0], 
        "EEST" : [3, 0],
        "EET" : [2, 0],
        "EGT" : [-1, 0],
        "EIT" : [9, 0],
        "EST" : [-5, 0],
        "FET" : [3, 0],
        "FJT" : [12, 0], 
        "FKST" : [-3, 0],
        "FKT" : [-4, 0],
        "FNT" : [-2, 0],
        "GALT" : [-6, 0],
        "GAMT" : [-9, 0], 
        "GET" : [4, 0],
        "GFT" : [-3, 0],
        "GILT" : [12, 0],
        "GIT" : [-9, 0],
        "GST" : [4, 0], 
        "GST2" : [-2, 0],
        "GYT" : [-4, 0],
        "HDT" : [9, 0], 
        "HAEC" : [2, 0], 
        "HST" : [-10, 0],
        "HKT" : [8, 0],
        "HMT" : [5, 0], 
        "HOVST" : [8, 0], 
        "HOVT" : [7, 0], 
        "ICT" : [7, 0],
        "IDLW" : [-12, 0],
        "IDT" : [3, 0],
        "IOT" : [3, 0],
        "IRDT" : [4, 30],
        "IRKT" : [8, 0],
        "IRST" : [3, 30], 
        "IST" : [2, 0],
        "IST2" : [1, 0],
        "IST3" : [5, 30],
        "JST" : [9, 0], 
        "KALT" : [2, 0],
        "KGT" : [6, 0],
        "KOST" : [11, 0],
        "KRAT" : [7, 0],
        "KST" : [9, 0],
        "LHST" : [10, 30],
        "LINT" : [14, 0],
        "MAGT" : [12, 0],
        "MART" : [-9, -30],
        "MAWT" : [5, 0], 
        "MDT" : [-6, 0], 
        "MET" : [1, 0], 
        "MEST" : [2, 0], 
        "MHT" : [12, 0], 
        "MIST" : [11, 0], 
        "MIT" : [-9, -30],
        "MMT" : [6, 30], 
        "MSK" : [3, 0], 
        "MST" : [-7, 0], 
        "MST2" : [8, 0],
        "MUT" : [4, 0],
        "MVT" : [5, 0], 
        "MYT" : [8, 0], 
        "NCT" : [11, 0],
        "NDT" : [-2, -30], 
        "NFT" : [11, 0],
        "NOVT" : [7, 0],
        "NPT" : [5, 45],
        "NST" : [-3, -30],
        "NT" : [-3, -30],
        "NUT" : [-11, 0],
        "NZDT" : [13, 0],
        "NZST" : [12, 0],
        "OMST" : [6, 0],
        "ORAT" : [5, 0], 
        "PDT" : [-7, 0], 
        "PETT" : [12, 0],
        "PGT" : [10, 0], 
        "PHOT" : [13, 0],
        "PHT" : [8, 0],
        "PKT" : [5, 0], 
        "PMDT" : [-2, 0],
        "PMST" : [-3, 0], 
        "PONT" : [11, 0], 
        "PST" : [-8, 0],
        "PST2" : [8, 0],
        "PYST" : [-3, 0],
        "PYT" : [-4, 0],
        "RET" : [4, 0],
        "ROTT" : [-3, 0],
        "SAKT" : [11, 0],
        "SAMT" : [4, 0],
        "SAST" : [2, 0],
        "SBT" : [11, 0],
        "SCT" : [4, 0], 
        "SDT" : [-10, 0], 
        "SGT" : [8, 0], 
        "SLST" : [5, 30], 
        "SRET" : [11, 0],
        "SRT" : [-3, 0],
        "SST" : [-11, 0],
        "SST2" : [8, 0],
        "SYOT" : [3, 0],
        "TAHT" : [-10, 0],
        "THA" : [7, 0], 
        "TFT" : [5, 0], 
        "TJT" : [5, 0], 
        "TKT" : [13, 0], 
        "TLT" : [9, 0], 
        "TMT" : [5, 0], 
        "TRT" : [3, 0],
        "TOT" : [13, 0],
        "TVT" : [12, 0],
        "ULAST" : [9, 0],
        "UTC" : [0, 0], 
        "UYST" : [-2, 0], 
        "UYT" : [-3, 0],
        "UZT" : [5, 0], 
        "VET" : [-4, 0], 
        "VLAT" : [10, 0], 
        "VOLT" : [4, 0], 
        "VOST" : [6, 0], 
        "VUT" : [11, 0],
        "WAKT" : [12, 0],
        "WAST" : [2, 0],
        "WAT" : [1, 0],
        "WEST" : [1,0],
        "WIT" : [7, 0],
        "WST" : [8, 0], 
        "YAKT" : [9, 0], 
        "YEKT" : [5, 0]
    }

    military_time = to_bool(military_time)
    if isinstance(military_time, str): 
        military_time = False

    time_zone = str(time_zone)
    time_zone = time_zone.upper()
    local_time = time.gmtime(time.time())

    if time_zone in time_zones.keys() and return_time: 
        offset = time_zones[time_zone]
        hour = local_time[3]
        minute = local_time[4]

        hour += offset[0]
        minute += offset[1]

        if minute > 60: 
            minute -= 60
            hour += 1
        elif minute < 0: 
            minute += 60
            hour -= 1
        
        if hour > 24: 
            hour -= 24

        elif hour < 0: 
            hour += 24
        
        if not military_time and hour > 12: 
                hour -= 12
        
        time_list = [hour, minute, local_time[5]]

        return time_list
    elif return_time: 
        time_list = [local_time[3], local_time[4], local_time[5]]
        return time_list
    elif not return_time: 
        return "Error"

def to_time_zone(arg):
    try: 
        arg = time_zone.TimeZone(arg)
    except: 
        arg = arg
    
    return arg


class EastHelpCommand(discord.ext.commands.HelpCommand):
    cog_list = ["Commands", "DevCommands", "AdminCommands", "JokeCommands"]
    def get_destination(self): 
        #TODO: Make DMs a valid option
        ctx = self.context 
        return ctx.channel

    async def server_prefix(self):
        return (await self.context.bot.get_prefix(self.context))[0]
    
    async def gen_command_signature(self, command): 
        parent_command = command.full_parent_name 
        if parent_command: 
            return f"{await self.server_prefix()}{parent_command} {command.name} {command.signature}"
        else: 
            return f"{await self.server_prefix()}{command.name} {command.signature}"

    async def command_help(self, command, embed, signature = False): 
        if signature:
            embed.add_field(name = "Signature", value = await self.gen_command_signature(command))
            embed.add_field(name = "Documentation", value = command.help, inline = False)
        else: 
            embed.add_field(name = command.name, value = command.description, inline = False)
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title = "Help", color = 0xff0000)
        for cog in mapping: 
            if cog is None: 
                continue 

            if cog.qualified_name == "DevCommands": 
                continue 
            
            embed.add_field(name = cog.qualified_name, value = cog.description, inline = False)
        await self.get_destination().send(embed = embed)

    async def send_cog_help(self, cog): 
        embed = discord.Embed(title = "Help", color = 0xff0000)
        embed.description = cog.description
        for command in cog.get_commands(): 
            await self.command_help(command, embed)
        await self.get_destination().send(embed = embed)

    async def send_group_help(self, group): 
        embed = discord.Embed(title = "Help", color = 0xff0000)
        embed.description = group.description
        await self.command_help(group, embed, True)
        content = ""
        for command in group.commands: 
            content += f"{command.name}: {command.description}\n"

        embed.add_field(name = "Subcommands", value = content)
        await self.get_destination().send(embed = embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title = "Help", color = 0xff0000)
        await self.command_help(command, embed, True)
        await self.get_destination().send(embed = embed)

    

