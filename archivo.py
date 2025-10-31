# pip install rx  
from rx.subject import Subject
from typing import Callable, Dict


class ConcreteObserverA:
    def __init__(self, name="ObserverA"):
        self.name = name

    def on_next(self, value):
        print(f"[{self.name}] recibió: {value}")

    def on_error(self, err):
        print(f"[{self.name}] error: {err}")

    def on_completed(self):
        print(f"[{self.name}] stream completado")


class ConcreteObserverB(ConcreteObserverA):
    def __init__(self):
        super().__init__(name="ObserverB")



class MySubject:
    def __init__(self):
        self._subject = Subject()
        # guardamos los disposables para poder desuscribir
        self._subscriptions: Dict[object, object] = {}

    def registerObserver(self, observer: ConcreteObserverA):
        """Se suscribe y guarda el disposable."""
        disp = self._subject.subscribe(
            on_next=observer.on_next,
            on_error=observer.on_error,
            on_completed=observer.on_completed,
        )
        self._subscriptions[observer] = disp

    def unregisterObserver(self, observer: ConcreteObserverA):
        """Cancela la suscripción (dispose)."""
        disp = self._subscriptions.pop(observer, None)
        if disp:
            disp.dispose()

    def notifyObservers(self, value):
        """Emite un valor a todos los observers suscritos."""
        self._subject.on_next(value)

    
    def complete(self):
        self._subject.on_completed()

    def error(self, exc: Exception):
        self._subject.on_error(exc)



if __name__ == "__main__":
    subject = MySubject()

    a = ConcreteObserverA()
    b = ConcreteObserverB()

    subject.registerObserver(a)
    subject.registerObserver(b)

    # Notificar (on_next)
    subject.notifyObservers("Evento #1")
    subject.notifyObservers({"tipo": "update", "valor": 42})

    # Desuscribir a B y seguir notificando
    subject.unregisterObserver(b)
    subject.notifyObservers("Solo lo ve A")

    # Completar el stream
    subject.complete()
