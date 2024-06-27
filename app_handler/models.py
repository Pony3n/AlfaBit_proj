from django.db import models


class LeadState(models.Model):
    # pk экземпляров модели
    STATE_NEW = 1 # Новый
    STATE_IN_PROGRESS = 2 # В работе
    STATE_POSTPONED = 3 # Приостановлен
    STATE_DONE = 4 # Завершен

    name = models.CharField(
        u"Название",
        max_length=50,
        unique=True,
    )


class Lead(models.Model):

    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=u"Имя",
    )

    state = models.ForeignKey(
        LeadState,
        on_delete=models.PROTECT,
        default=LeadState.STATE_NEW,
        verbose_name=u"Состояние",
    )

    def _execute_business_logic_for_transition(self, from_state, to_state):
        method_name = f"on_transition_{from_state}_to_{to_state}"
        method = getattr(self, method_name, None)
        if method:
            method()

    def change_state(self, new_state):
        valid_transitions = {
            LeadState.STATE_NEW: [LeadState.STATE_IN_PROGRESS],
            LeadState.STATE_IN_PROGRESS: [LeadState.STATE_POSTPONED, LeadState.STATE_DONE],
            LeadState.STATE_POSTPONED: [LeadState.STATE_IN_PROGRESS, LeadState.STATE_DONE]
        }

        current_state_id = self.state.id
        if new_state not in valid_transitions.get(current_state_id, []):
            raise ValueError("Недопустимый переход состояния")

        old_state = self.state_id
        self.state_id = new_state
        self.save()

        self._execute_business_logic_for_transition(old_state, new_state)

    def on_transition_1_to_2(self):
        print('Новый -> В работе')
        print('Поменял статус. Отправил пользователю сообщение на почту\n')

    def on_transition_2_to_3(self):
        print('В работе -> Приостановлен')
        print('\n')


    def on_transition_2_to_4(self):
        print('В работе -> Завершен')
        print('\n')

    def on_transition_3_to_2(self):
        print('Приостановлен -> В работе')
        print('\n')


    def on_transition_3_to_4(self):
        print('Приостановлен -> Завершен')
        print('\n')
