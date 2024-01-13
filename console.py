#!/usr/bin/python3
""" module that contains the entry point ofthe program"""

import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """contains functionality of HBNB console"""

    prompt = '(hbnb) 'if sys.__stdin__.isatty() else ''
    
    storage = FileStorage()

    classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax"""
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) == dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Handles EOF to exit the program"""
        return True

    def emptyline(self):
        """Overides the emptyline method"""
        return False
    
    def do_create(self, line):
        """Creates a new instance of BM, saves to JSON and prints the id """
        from models import storage
        if not line:
            print("** class name missing **")
        elif line not in storage.classes:
            print("** class doesn't exist **")
        else:
            result = storage.classes[line]()
            models.storage.save()
            print(result.id)

    def do_show(self, args):
        """method to show objects"""
        n = args.partition(" ")
        ob_name = n[0]
        ob_id = n[2]

        if ob_id and ' ' in ob_id:
            ob_id = ob_id.partition(' ')[0]

        if not ob_name:
            print("** class name missing **")
            return

        if ob_name not in HBNBCommand.classes:
            print("** class doen't exist **")
            return

        if not ob_id:
            print("** instance id missing **")
            return

        key = ob_name + "." + ob_id

        try:
            print(HBNBCommand.storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """Destroys indicated object"""
        n = args.partition(" ")
        ob_name = n[0]
        ob_id = n[2]

        if ob_id and ' ' in ob_id:
            ob_id = ob_id.partition(' ')[0]

        if not ob_name:
            print("** class name missing **")
            return

        if ob_name not in HBNBCommand.classes:
            print("** class doen't exist **")
            return

        if not ob_id:
            print("** instance id missing **")
            return

        key = ob_name + "." + ob_id

        try:
            del(HBNBCommand.storage.all()[key])
            HBNBCommand.storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        """method that shows all objects"""
        print_list = []

        if args:
            args = args.split(' ')[0]
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for a, b in HBNBCommand.storage._FileStorage__objects.items():
                if a.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for a, b in HBNBCommand.storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)



    def do_update(self, args):
        """updates objects with new info"""
        ob_name = ob_id = attr_name = attr_val = kwargs = ''

        args = args.partition(" ")
        if args[0]:
            ob_name = args[0]
        else:
            print("** class name is missing **")
            return

        if ob_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        args = args[2].partition(" ")
        if args[0]:
            ob_id = args[0]
        else:
            print("** instance id is missing **")
            return

        key = ob_name + "." + ob_id

        if key not in HBNBCommand.storage.all():
            print("** no instance found **")
            return
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []

            for a, b in kwargs.items():
                args.append(a)
                args.append(b)
        else:
            args = args[2]
            if args and args[0] == '\"':
                s_qt = arggs.find('\"', 1)
                attr_name = args[1:s_qt]
                args = args[s_qt + 1:]

            args = args.partition(' ')

            if not attr_name and args[0] != ' ':
                attr_name = args[0]

            if args[2] and args[2][0] == '\"':
                attr_val = args[2][1:args[2].find('\"', 1)]

            if not attr_val and args[2]:
                attr_val = args[2].partition(' ')[0]

            args = [attr_name, attr_val]

        new_dict = HBNBCommand.storage.all()[key]

        for i, attr_name in enumerate(args):
            if (i % 2 == 0):
                attr_val = args[i + 1]
                if not attr_name:
                    print("** attribute name missing **")
                    return
                if not attr_val:
                    print("** value missing **")
                    return
                if attr_name in HBNBCommand.types:
                    attr_val = HBNBCommand.types[attr_name](attr_val)

                new_dict.__dict__.update({attr_name: attr_val})

        new_dict.save()

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for a, b in HBNBCommand.storage._FileStorage__objects.items():
            if args == a.split('.')[0]:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
