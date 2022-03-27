from django.db import models

class Blindbox(models.Model):
    boxid = models.IntegerField(db_column='boxID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=50)
    b_price = models.DecimalField(max_digits=10, decimal_places=2)
    description= models.CharField(max_length=500,null=True)
    b_pic = models.CharField(max_length=500,null=True)
    class Meta:
        managed = True
        db_table = 'blindbox'


class Boxorder(models.Model):
    b_orderid = models.IntegerField(db_column='b_orderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='userID')  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, on_delete=models.CASCADE, db_column='boxID')  # Field name made lowercase.
    pay_datetime = models.CharField(max_length=50)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'boxorder'


class Card(models.Model):
    cardno = models.IntegerField(db_column='cardNO', primary_key=True)  # Field name made lowercase.
    rarity = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    img = models.CharField(max_length=500)
    type = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'card'


class Contain(models.Model):
    cardno = models.OneToOneField(Card,on_delete=models.CASCADE, db_column='cardNO', primary_key=True)  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, on_delete=models.CASCADE, db_column='boxID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'contain'
        unique_together = (('cardno', 'boxid'),)


class Ownedcard(models.Model):
    cardid = models.IntegerField(db_column='cardID', primary_key=True)  # Field name made lowercase.
    cardno = models.ForeignKey(Card,on_delete=models.CASCADE, db_column='cardNO')  # Field name made lowercase.
    userid = models.ForeignKey('User',on_delete=models.CASCADE, db_column='userID')  # Field name made lowercase.
    status = models.CharField(max_length=50)
    c_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'ownedcard'


class Probability(models.Model):
    ruleno = models.IntegerField(db_column='ruleNO', primary_key=True)  # Field name made lowercase.
    boxid = models.ForeignKey(Blindbox, on_delete=models.CASCADE, db_column='boxID')  # Field name made lowercase.
    rarity = models.CharField(max_length=50)
    prob = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        managed = True
        db_table = 'probability'


class Resaleorder(models.Model):
    r_orderid = models.IntegerField(db_column='r_orderID', primary_key=True)  # Field name made lowercase.
    sellerid = models.ForeignKey('User', related_name='sellerid', on_delete=models.CASCADE, db_column='sellerID')  # Field name made lowercase.
    buyerid = models.ForeignKey('User', related_name='buyerid',on_delete=models.CASCADE, db_column='buyerID')  # Field name made lowercase.
    cardid = models.ForeignKey(Ownedcard, on_delete=models.CASCADE, db_column='cardID')  # Field name made lowercase.
    trade_amount = models.DecimalField(max_digits=10, decimal_places=2)
    trade_datetime = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'resaleorder'


class User(models.Model):
    userid = models.IntegerField(db_column='userID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=50)
    u_name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'user'
