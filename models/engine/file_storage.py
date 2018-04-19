#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary if cls == None, else return a dictionary of
            all classes of type cls
        '''
        objs = {}
        if cls is None:
            return self.__objects
        if isinstance(cls, str):
            cls = models.classes[cls]
        for key, val in FileStorage.__objects.items():
            if cls.__name__ == val.__class__.__name__:
                objs[key] = val
        return objs

    def new(self, obj):
        '''
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                objects = json.load(fd)
            for key, val in objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                if "id" in val:
                    obj_id = val["id"]
                new = class_name(**val)
                key = str(class_name.__name__) + '.' + str(new.id)
                FileStorage.__objects[key] = new
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
            Deletes obj from __objects if it is there
        '''
        if not obj:
            return
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()

    def close(self):
        '''
            Calls reload method
        '''
        self.reload()
